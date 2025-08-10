"""
VM module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class VMModule:
    """Module for handling VM spawning-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def spawn_vm(self, machine_id: int) -> Dict[str, Any]:
        """Spawn a virtual machine"""
        return self.api.post("/vm/spawn", json_data={"machine_id": machine_id})
    
    def extend_vm(self, machine_id: int) -> Dict[str, Any]:
        """Extend the virtual machine"""
        return self.api.post("/vm/extend", json_data={"machine_id": machine_id})
    
    def reset_vm(self, machine_id: int) -> Dict[str, Any]:
        """Reset the virtual machine"""
        return self.api.post("/vm/reset", json_data={"machine_id": machine_id})
    
    def terminate_vm(self, machine_id: int) -> Dict[str, Any]:
        """Terminate the virtual machine"""
        return self.api.post("/vm/terminate", json_data={"machine_id": machine_id})
    
    def vote_reset_vm(self, machine_id: int) -> Dict[str, Any]:
        """Vote to reset the virtual machine"""
        return self.api.post("/vm/reset/vote", json_data={"machine_id": machine_id})
    
    def accept_reset_vote(self, machine_id: int) -> Dict[str, Any]:
        """Accept vote to reset the virtual machine"""
        return self.api.post("/vm/reset/vote/accept", json_data={"machine_id": machine_id})

# Click commands
@click.group()
def vm():
    """VM spawning-related commands"""
    pass

@vm.command()
@click.argument('machine_id', type=int)
def spawn(machine_id):
    """Spawn a virtual machine"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.spawn_vm(machine_id)
        
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
@click.argument('machine_id', type=int)
def extend(machine_id):
    """Extend the virtual machine"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.extend_vm(machine_id)
        
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
@click.argument('machine_id', type=int)
def reset(machine_id):
    """Reset the virtual machine"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.reset_vm(machine_id)
        
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
@click.argument('machine_id', type=int)
def terminate(machine_id):
    """Terminate the virtual machine"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.terminate_vm(machine_id)
        
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
@click.argument('machine_id', type=int)
def vote_reset(machine_id):
    """Vote to reset the virtual machine"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.vote_reset_vm(machine_id)
        
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
@click.argument('machine_id', type=int)
def accept_vote(machine_id):
    """Accept vote to reset the virtual machine"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.accept_reset_vote(machine_id)
        
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
