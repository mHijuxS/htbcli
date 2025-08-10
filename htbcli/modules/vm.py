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
    
    def get_vm_info(self) -> Dict[str, Any]:
        """Get VM info"""
        return self.api.get("/vm/info")
    
    def get_vm_list(self) -> Dict[str, Any]:
        """Get VM list"""
        return self.api.get("/vm/list")
    
    def get_vm_terminals(self) -> Dict[str, Any]:
        """Get VM terminals"""
        return self.api.get("/vm/terminals")
    
    def get_vm_terminals_list(self) -> Dict[str, Any]:
        """Get VM terminals list"""
        return self.api.get("/vm/terminals/list")
    
    def get_vms(self) -> Dict[str, Any]:
        """Get VMs (alternative endpoint)"""
        return self.api.get("/vms")
    
    def get_vms_info(self) -> Dict[str, Any]:
        """Get VMs info (alternative endpoint)"""
        return self.api.get("/vms/info")

# Click commands
@click.group()
def vm():
    """VM spawning-related commands"""
    pass

@vm.command()
def info():
    """Get VM info"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.get_vm_info()
        
        if result and 'data' in result:
            info_data = result['data']
            console.print(Panel.fit(
                f"[bold green]VM Info[/bold green]\n"
                f"Status: {info_data.get('status', 'N/A') or 'N/A'}\n"
                f"Type: {info_data.get('type', 'N/A') or 'N/A'}\n"
                f"Region: {info_data.get('region', 'N/A') or 'N/A'}\n"
                f"IP: {info_data.get('ip', 'N/A') or 'N/A'}",
                title="VM Info"
            ))
        else:
            console.print("[yellow]No VM info found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_vm():
    """Get VM list"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.get_vm_list()
        
        if result and 'data' in result:
            list_data = result['data']
            
            table = Table(title="VM List")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Region", style="blue")
            table.add_column("IP", style="red")
            
            for vm in list_data:
                table.add_row(
                    str(vm.get('id', 'N/A') or 'N/A'),
                    str(vm.get('name', 'N/A') or 'N/A'),
                    str(vm.get('status', 'N/A') or 'N/A'),
                    str(vm.get('type', 'N/A') or 'N/A'),
                    str(vm.get('region', 'N/A') or 'N/A'),
                    str(vm.get('ip', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No VM list found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
def terminals():
    """Get VM terminals"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.get_vm_terminals()
        
        if result and 'data' in result:
            terminals_data = result['data']
            
            table = Table(title="VM Terminals")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Created", style="blue")
            
            for terminal in terminals_data:
                table.add_row(
                    str(terminal.get('id', 'N/A') or 'N/A'),
                    str(terminal.get('name', 'N/A') or 'N/A'),
                    str(terminal.get('status', 'N/A') or 'N/A'),
                    str(terminal.get('type', 'N/A') or 'N/A'),
                    str(terminal.get('created_at', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No terminals found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
def terminals_list():
    """Get VM terminals list"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.get_vm_terminals_list()
        
        if result and 'data' in result:
            terminals_list_data = result['data']
            
            table = Table(title="VM Terminals List")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Region", style="blue")
            
            for terminal in terminals_list_data:
                table.add_row(
                    str(terminal.get('id', 'N/A') or 'N/A'),
                    str(terminal.get('name', 'N/A') or 'N/A'),
                    str(terminal.get('status', 'N/A') or 'N/A'),
                    str(terminal.get('type', 'N/A') or 'N/A'),
                    str(terminal.get('region', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No terminals list found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
def vms():
    """Get VMs (alternative endpoint)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.get_vms()
        
        if result and 'data' in result:
            vms_data = result['data']
            
            table = Table(title="VMs (Alternative)")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Region", style="blue")
            
            for vm in vms_data:
                table.add_row(
                    str(vm.get('id', 'N/A') or 'N/A'),
                    str(vm.get('name', 'N/A') or 'N/A'),
                    str(vm.get('status', 'N/A') or 'N/A'),
                    str(vm.get('type', 'N/A') or 'N/A'),
                    str(vm.get('region', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No VMs found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@vm.command()
def vms_info():
    """Get VMs info (alternative endpoint)"""
    try:
        api_client = HTBAPIClient()
        vm_module = VMModule(api_client)
        result = vm_module.get_vms_info()
        
        if result and 'data' in result:
            vms_info_data = result['data']
            console.print(Panel.fit(
                f"[bold green]VMs Info (Alternative)[/bold green]\n"
                f"Status: {vms_info_data.get('status', 'N/A') or 'N/A'}\n"
                f"Type: {vms_info_data.get('type', 'N/A') or 'N/A'}\n"
                f"Region: {vms_info_data.get('region', 'N/A') or 'N/A'}\n"
                f"Count: {vms_info_data.get('count', 'N/A') or 'N/A'}",
                title="VMs Info"
            ))
        else:
            console.print("[yellow]No VMs info found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
