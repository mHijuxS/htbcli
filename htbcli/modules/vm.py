"""
VM module for HTB CLI
"""

import click
import time
from typing import Dict, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option
from .machines import MachinesModule
from .connection import ConnectionModule

console = Console()

class VMModule:
    """Module for handling VM spawning-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
        self.machines_module = MachinesModule(api_client)
        self._machine_id_cache = {}  # Cache for machine name to ID resolution
    
    def resolve_machine_id(self, machine_identifier: Union[int, str]) -> Optional[int]:
        """Resolve machine identifier to machine ID"""
        if isinstance(machine_identifier, int):
            return machine_identifier
        elif isinstance(machine_identifier, str):
            # Try to convert to int first (in case it's a string number)
            try:
                return int(machine_identifier)
            except ValueError:
                # Check cache first
                if machine_identifier in self._machine_id_cache:
                    machine_id = self._machine_id_cache[machine_identifier]
                    console.print(f"[blue]Using cached machine ID: {machine_id} for '{machine_identifier}'[/blue]")
                    return machine_id
                
                # Search for machine by name
                console.print(f"[blue]Searching for machine: {machine_identifier}[/blue]")
                machine_id = self.machines_module.search_machine_by_name(machine_identifier)
                if machine_id:
                    console.print(f"[green]✓[/green] Found machine ID: {machine_id} for '{machine_identifier}'")
                    # Cache the result
                    self._machine_id_cache[machine_identifier] = machine_id
                    return machine_id
                else:
                    console.print(f"[red]Could not find machine with name: {machine_identifier}[/red]")
                    return None
        else:
            console.print(f"[red]Invalid machine identifier type: {type(machine_identifier)}[/red]")
            return None
    
    def check_machine_status(self, machine_identifier: Union[int, str]) -> Dict[str, Any]:
        """Check machine status to determine if it's free or VIP"""
        try:
            # Get machine profile to check if it's free
            if isinstance(machine_identifier, str):
                # If it's a string, assume it's a machine name/slug
                result = self.machines_module.get_machine_profile(machine_identifier)
            else:
                # If it's an int, we need to get the machine name first
                # For now, we'll just return a generic response
                return {"free": False, "message": "Machine status check not available for ID"}
            
            if result and 'info' in result:
                info = result['info']
                is_free = info.get('free', False)
                return {
                    "free": is_free,
                    "name": info.get('name', machine_identifier),
                    "status": "Free" if is_free else "VIP"
                }
            else:
                return {"free": False, "message": "Could not determine machine status"}
        except Exception as e:
            return {"free": False, "message": f"Error checking machine status: {str(e)}"}

    def spawn_vm(self, machine_identifier: Union[int, str]) -> Dict[str, Any]:
        """Spawn a virtual machine"""
        # If it's already an integer, use it directly
        if isinstance(machine_identifier, int):
            machine_id = machine_identifier
        else:
            # Otherwise resolve it
            machine_id = self.resolve_machine_id(machine_identifier)
            if machine_id is None:
                return {"error": "Could not resolve machine identifier"}
        return self.api.post("/vm/spawn", json_data={"machine_id": machine_id})
    
    def wait_for_vm_ready(self, machine_identifier: Union[int, str], max_wait_time: int = 300) -> Dict[str, Any]:
        """Wait for VM to be ready by polling status every 5 seconds"""
        # If it's already an integer, use it directly
        if isinstance(machine_identifier, int):
            machine_id = machine_identifier
        else:
            # Otherwise resolve it
            machine_id = self.resolve_machine_id(machine_identifier)
            if machine_id is None:
                return {"error": "Could not resolve machine identifier"}
        
        console.print(f"[blue]Waiting for VM to be ready... (max wait time: {max_wait_time}s)[/blue]")
        
        start_time = time.time()
        attempts = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Checking VM status...", total=None)
            
            while time.time() - start_time < max_wait_time:
                attempts += 1
                progress.update(task, description=f"Checking VM status... (attempt {attempts})")
                
                try:
                    # Get VM status
                    vm_status = self.machines_module.get_vm_status()
                    
                    if vm_status and vm_status.get('info'):
                        info = vm_status['info']
                        is_spawning = info.get('isSpawning', True)
                        ip_address = info.get('ip')
                        
                        # Check if VM is ready (not spawning and has IP)
                        if not is_spawning and ip_address:
                            progress.update(task, description="VM is ready!")
                            console.print(f"\n[bold green]✓ VM is ready![/bold green]")
                            console.print(f"[green]IP Address: {ip_address}[/green]")
                            console.print(f"[green]Machine: {info.get('name', 'N/A')}[/green]")
                            console.print(f"[green]Expires at: {info.get('expires_at', 'N/A')}[/green]")
                            return {
                                "success": True,
                                "ip": ip_address,
                                "machine_name": info.get('name'),
                                "expires_at": info.get('expires_at'),
                                "wait_time": time.time() - start_time,
                                "attempts": attempts
                            }
                        elif is_spawning:
                            progress.update(task, description=f"VM is spawning... (attempt {attempts})")
                        elif not ip_address:
                            progress.update(task, description=f"Waiting for IP address... (attempt {attempts})")
                    else:
                        progress.update(task, description=f"No VM status found... (attempt {attempts})")
                
                except Exception as e:
                    progress.update(task, description=f"Error checking status: {str(e)}... (attempt {attempts})")
                
                # Wait 5 seconds before next check
                time.sleep(5)
        
        # If we get here, we've timed out
        console.print(f"\n[red]Timeout: VM did not become ready within {max_wait_time} seconds[/red]")
        return {
            "error": f"Timeout: VM did not become ready within {max_wait_time} seconds",
            "wait_time": max_wait_time,
            "attempts": attempts
        }
    
    def extend_vm(self, machine_identifier: Union[int, str]) -> Dict[str, Any]:
        """Extend the virtual machine"""
        machine_id = self.resolve_machine_id(machine_identifier)
        if machine_id is None:
            return {"error": "Could not resolve machine identifier"}
        return self.api.post("/vm/extend", json_data={"machine_id": machine_id})
    
    def reset_vm(self, machine_identifier: Union[int, str]) -> Dict[str, Any]:
        """Reset the virtual machine"""
        machine_id = self.resolve_machine_id(machine_identifier)
        if machine_id is None:
            return {"error": "Could not resolve machine identifier"}
        return self.api.post("/vm/reset", json_data={"machine_id": machine_id})
    
    def terminate_vm(self, machine_identifier: Union[int, str]) -> Dict[str, Any]:
        """Terminate the virtual machine"""
        machine_id = self.resolve_machine_id(machine_identifier)
        if machine_id is None:
            return {"error": "Could not resolve machine identifier"}
        return self.api.post("/vm/terminate", json_data={"machine_id": machine_id})
    
    def vote_reset_vm(self, machine_identifier: Union[int, str]) -> Dict[str, Any]:
        """Vote to reset the virtual machine"""
        machine_id = self.resolve_machine_id(machine_identifier)
        if machine_id is None:
            return {"error": "Could not resolve machine identifier"}
        return self.api.post("/vm/reset/vote", json_data={"machine_id": machine_id})
    
    def accept_reset_vote(self, machine_identifier: Union[int, str]) -> Dict[str, Any]:
        """Accept vote to reset the virtual machine"""
        machine_id = self.resolve_machine_id(machine_identifier)
        if machine_id is None:
            return {"error": "Could not resolve machine identifier"}
        return self.api.post("/vm/reset/vote/accept", json_data={"machine_id": machine_id})

# Click commands
@click.group()
def vm():
    """VM spawning-related commands"""
    pass

@vm.command()
@click.argument('machine_identifier')
@click.option('--no-wait', is_flag=True, help='Do not wait for VM to be ready (spawn and exit immediately)')
@click.option('--max-wait', default=300, help='Maximum wait time in seconds (default: 300)')
@click.option('--vpn-server', type=int, help='VPN server ID to use for spawning (use "vm vpn-servers" to see available servers)')
def spawn(machine_identifier, no_wait, max_wait, vpn_server):
    """Spawn a virtual machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        
        # Switch VPN server if specified
        if vpn_server:
            console.print(f"[blue]Switching to VPN server ID: {vpn_server}[/blue]")
            try:
                connection_module = ConnectionModule(api_client)
                switch_result = connection_module.switch_vpn_server(vpn_server)
                if switch_result and switch_result.get('status') == True:
                    console.print(f"[green]✓ Successfully switched to VPN server {vpn_server}[/green]")
                else:
                    console.print(f"[yellow]Warning: VPN server switch may have failed: {switch_result}[/yellow]")
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to switch VPN server: {e}[/yellow]")
                console.print("[yellow]Continuing with VM spawn...[/yellow]")
        
        # Check machine status first
        status_check = vm_module.check_machine_status(machine_identifier)
        if status_check.get('free') is False and status_check.get('status') == 'VIP':
            console.print(f"[yellow]Warning: {status_check.get('name', machine_identifier)} is a VIP machine[/yellow]")
            console.print("[yellow]VIP machines require a VIP subscription to spawn[/yellow]")
            console.print("[yellow]You may encounter an error if you don't have VIP access[/yellow]\n")
        
        # Resolve machine ID once
        machine_id = vm_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Error: Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        # First spawn the VM
        result = vm_module.spawn_vm(machine_id)
        
        if result and 'error' in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        if result and 'message' in result:
            console.print(Panel.fit(
                f"[bold green]VM Spawned Successfully[/bold green]\n"
                f"Message: {result['message']}",
                title="VM Spawn"
            ))
        else:
            console.print("[yellow]No response from VM spawn[/yellow]")
        
        # Wait for VM to be ready by default, unless --no-wait flag is provided
        if not no_wait:
            console.print("\n[blue]Waiting for VM to be ready...[/blue]")
            wait_result = vm_module.wait_for_vm_ready(machine_id, max_wait)
            
            if wait_result.get('success'):
                console.print(Panel.fit(
                    f"[bold green]VM Ready![/bold green]\n"
                    f"IP Address: {wait_result['ip']}\n"
                    f"Machine: {wait_result['machine_name']}\n"
                    f"Expires at: {wait_result['expires_at']}\n"
                    f"Wait time: {wait_result['wait_time']:.1f}s\n"
                    f"Attempts: {wait_result['attempts']}",
                    title="VM Ready"
                ))
            else:
                console.print(f"[red]Error waiting for VM: {wait_result.get('error', 'Unknown error')}[/red]")
        else:
            console.print("\n[yellow]Skipping wait - use 'vm wait <machine>' to check status later[/yellow]")
                
    except Exception as e:
        error_msg = str(e)
        
        # Handle specific VM spawn errors
        if "Cannot spawn non-free machine on a free server" in error_msg:
            console.print(f"[red]Error: {error_msg}[/red]")
            console.print("\n[yellow]This error occurs because:[/yellow]")
            console.print("• You're trying to spawn a VIP machine on a free server")
            console.print("• VIP machines require a VIP subscription to spawn")
            console.print("\n[blue]Solutions:[/blue]")
            console.print("• Upgrade to VIP subscription to spawn VIP machines")
            console.print("• Try spawning a free machine instead")
            console.print("• Check machine status with: htbcli machines profile <machine_name>")
        else:
            console.print(f"[red]Error: {error_msg}[/red]")

@vm.command()
@click.argument('machine_identifier')
@click.option('--max-wait', default=300, help='Maximum wait time in seconds (default: 300)')
def wait(machine_identifier, max_wait):
    """Wait for VM to be ready (poll every 5 seconds until isSpawning=False and IP is available)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        
        console.print(f"[blue]Waiting for VM to be ready...[/blue]")
        wait_result = vm_module.wait_for_vm_ready(machine_identifier, max_wait)
        
        if wait_result.get('success'):
            console.print(Panel.fit(
                f"[bold green]VM Ready![/bold green]\n"
                f"IP Address: {wait_result['ip']}\n"
                f"Machine: {wait_result['machine_name']}\n"
                f"Expires at: {wait_result['expires_at']}\n"
                f"Wait time: {wait_result['wait_time']:.1f}s\n"
                f"Attempts: {wait_result['attempts']}",
                title="VM Ready"
            ))
        else:
            console.print(f"[red]Error waiting for VM: {wait_result.get('error', 'Unknown error')}[/red]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
@click.argument('machine_identifier')
def extend(machine_identifier):
    """Extend the virtual machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.extend_vm(machine_identifier)
        
        if result and 'error' in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        if result and 'message' in result:
            console.print(Panel.fit(
                f"[bold green]VM Extended Successfully[/bold green]\n"
                f"Message: {result['message']}\n"
                f"Expiration: {result.get('expirationDate', 'N/A')}",
                title="VM Extend"
            ))
        else:
            console.print("[yellow]No response from VM extend[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
@click.argument('machine_identifier', required=False)
def reset(machine_identifier):
    """Reset the virtual machine (accepts machine ID or name, defaults to active machine)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        
        # If no machine identifier provided, get the active machine
        if machine_identifier is None:
            vm_status = vm_module.machines_module.get_vm_status()
            if vm_status and vm_status.get('info'):
                active_info = vm_status['info']
                machine_identifier = active_info.get('name')
                if machine_identifier:
                    console.print(f"[blue]No machine specified, using active machine: {machine_identifier}[/blue]")
                else:
                    console.print("[red]Error: No active machine found and no machine specified[/red]")
                    return
            else:
                console.print("[red]Error: No active machine found and no machine specified[/red]")
                return
        
        result = vm_module.reset_vm(machine_identifier)
        
        if result and 'error' in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        if result and 'message' in result:
            console.print(Panel.fit(
                f"[bold green]VM Reset Successfully[/bold green]\n"
                f"Machine: {machine_identifier}\n"
                f"Message: {result['message']}",
                title="VM Reset"
            ))
        else:
            console.print("[yellow]No response from VM reset[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
@click.argument('machine_identifier', required=False)
def terminate(machine_identifier):
    """Terminate the virtual machine (accepts machine ID or name, defaults to active machine)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        
        # If no machine identifier provided, get the active machine
        if machine_identifier is None:
            vm_status = vm_module.machines_module.get_vm_status()
            if vm_status and vm_status.get('info'):
                active_info = vm_status['info']
                machine_identifier = active_info.get('name')
                if machine_identifier:
                    console.print(f"[blue]No machine specified, using active machine: {machine_identifier}[/blue]")
                else:
                    console.print("[red]Error: No active machine found and no machine specified[/red]")
                    return
            else:
                console.print("[red]Error: No active machine found and no machine specified[/red]")
                return
        
        result = vm_module.terminate_vm(machine_identifier)
        
        if result and 'error' in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        if result and 'message' in result:
            console.print(Panel.fit(
                f"[bold green]VM Terminated Successfully[/bold green]\n"
                f"Machine: {machine_identifier}\n"
                f"Message: {result['message']}",
                title="VM Terminate"
            ))
        else:
            console.print("[yellow]No response from VM terminate[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
@click.argument('machine_identifier')
def vote_reset(machine_identifier):
    """Vote to reset the virtual machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.vote_reset_vm(machine_identifier)
        
        if result and 'error' in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        if result and 'message' in result:
            console.print(Panel.fit(
                f"[bold green]Reset Vote Submitted[/bold green]\n"
                f"Message: {result['message']}",
                title="VM Reset Vote"
            ))
        else:
            console.print("[yellow]No response from reset vote[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
@click.argument('machine_identifier')
def accept_vote(machine_identifier):
    """Accept vote to reset the virtual machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.accept_reset_vote(machine_identifier)
        
        if result and 'error' in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        if result and 'message' in result:
            console.print(Panel.fit(
                f"[bold green]Reset Vote Accepted[/bold green]\n"
                f"Message: {result['message']}",
                title="VM Reset Vote Accept"
            ))
        else:
            console.print("[yellow]No response from vote accept[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def vpn_servers(debug, json_output):
    """List available VPN servers for VM spawning"""
    try:
        api_client = HTBAPIClient()
        connection_module = ConnectionModule(api_client)
        result = connection_module.get_connections_servers(params={"product": "labs"})
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: VPN Servers", json_output)
            return
        
        if result and 'data' in result:
            data = result['data']
            
            console.print("[bold blue]Available VPN Servers for VM Spawning[/bold blue]")
            console.print("[yellow]Use --vpn-server <ID> with vm spawn to select a server[/yellow]\n")
            
            table = Table(title="VPN Servers")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Location", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Clients", style="blue")
            table.add_column("Status", style="red")
            
            # Parse the nested structure
            if 'options' in data:
                for location, location_data in data['options'].items():
                    for type_name, type_data in location_data.items():
                        if 'servers' in type_data:
                            for server_id, server_info in type_data['servers'].items():
                                table.add_row(
                                    str(server_info.get('id', 'N/A')),
                                    str(server_info.get('friendly_name', 'N/A')),
                                    str(server_info.get('location', 'N/A')),
                                    str(type_name),
                                    str(server_info.get('current_clients', 'N/A')),
                                    "Full" if server_info.get('full', False) else "Available"
                                )
            
            console.print(table)
        else:
            console.print("[yellow]No VPN servers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
