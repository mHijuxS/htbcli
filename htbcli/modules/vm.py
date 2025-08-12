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
from .machines import MachinesModule

console = Console()

class VMModule:
    """Module for handling VM spawning-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
        self.machines_module = MachinesModule(api_client)
    
    def resolve_machine_id(self, machine_identifier: Union[int, str]) -> Optional[int]:
        """Resolve machine identifier to machine ID"""
        if isinstance(machine_identifier, int):
            return machine_identifier
        elif isinstance(machine_identifier, str):
            # Try to convert to int first (in case it's a string number)
            try:
                return int(machine_identifier)
            except ValueError:
                # Search for machine by name
                console.print(f"[blue]Searching for machine: {machine_identifier}[/blue]")
                machine_id = self.machines_module.search_machine_by_name(machine_identifier)
                if machine_id:
                    console.print(f"[green]✓[/green] Found machine ID: {machine_id} for '{machine_identifier}'")
                    return machine_id
                else:
                    console.print(f"[red]Could not find machine with name: {machine_identifier}[/red]")
                    return None
        else:
            console.print(f"[red]Invalid machine identifier type: {type(machine_identifier)}[/red]")
            return None
    
    def spawn_vm(self, machine_identifier: Union[int, str]) -> Dict[str, Any]:
        """Spawn a virtual machine"""
        machine_id = self.resolve_machine_id(machine_identifier)
        if machine_id is None:
            return {"error": "Could not resolve machine identifier"}
        return self.api.post("/vm/spawn", json_data={"machine_id": machine_id})
    
    def wait_for_vm_ready(self, machine_identifier: Union[int, str], max_wait_time: int = 300) -> Dict[str, Any]:
        """Wait for VM to be ready by polling status every 5 seconds"""
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
@click.option('--wait', is_flag=True, help='Wait for VM to be ready (poll every 5 seconds until isSpawning=False and IP is available)')
@click.option('--max-wait', default=300, help='Maximum wait time in seconds (default: 300)')
def spawn(machine_identifier, wait, max_wait):
    """Spawn a virtual machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        
        # First spawn the VM
        result = vm_module.spawn_vm(machine_identifier)
        
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
        
        # If --wait flag is provided, wait for VM to be ready
        if wait:
            console.print("\n[blue]Waiting for VM to be ready...[/blue]")
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
@click.argument('machine_identifier')
def reset(machine_identifier):
    """Reset the virtual machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.reset_vm(machine_identifier)
        
        if result and 'error' in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        if result and 'message' in result:
            console.print(Panel.fit(
                f"[bold green]VM Reset Successfully[/bold green]\n"
                f"Message: {result['message']}",
                title="VM Reset"
            ))
        else:
            console.print("[yellow]No response from VM reset[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
@click.argument('machine_identifier')
def terminate(machine_identifier):
    """Terminate the virtual machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.terminate_vm(machine_identifier)
        
        if result and 'error' in result:
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        if result and 'message' in result:
            console.print(Panel.fit(
                f"[bold green]VM Terminated Successfully[/bold green]\n"
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
