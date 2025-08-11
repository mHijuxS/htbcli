"""
VM module for HTB CLI
"""

import click
from typing import Dict, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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
def spawn(machine_identifier):
    """Spawn a virtual machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
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
