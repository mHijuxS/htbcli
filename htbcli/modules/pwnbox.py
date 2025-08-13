"""
PwnBox module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

class PwnBoxModule:
    """Module for handling PwnBox-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_pwnbox_info(self) -> Dict[str, Any]:
        """Get PwnBox info"""
        return self.api.get("/pwnbox/info")
    
    def get_pwnbox_list(self) -> Dict[str, Any]:
        """Get PwnBox list"""
        return self.api.get("/pwnbox/list")
    
    def get_pwnbox_terminals(self) -> Dict[str, Any]:
        """Get PwnBox terminals"""
        return self.api.get("/pwnbox/terminals")
    
    def get_pwnbox_terminals_list(self) -> Dict[str, Any]:
        """Get PwnBox terminals list"""
        return self.api.get("/pwnbox/terminals/list")

# Click commands
@click.group()
def pwnbox():
    """PwnBox-related commands"""
    pass

@pwnbox.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

def info(debug):
    """Get PwnBox info"""
    try:
        api_client = HTBAPIClient()
        pwnbox_module = PwnBoxModule(api_client)
        result = pwnbox_module.get_pwnbox_info()
        
        if result and 'data' in result:
            info_data = result['data']
            console.print(Panel.fit(
                f"[bold green]PwnBox Info[/bold green]\n"
                f"Status: {info_data.get('status', 'N/A') or 'N/A'}\n"
                f"Version: {info_data.get('version', 'N/A') or 'N/A'}\n"
                f"Region: {info_data.get('region', 'N/A') or 'N/A'}\n"
                f"IP: {info_data.get('ip', 'N/A') or 'N/A'}",
                title="PwnBox Info"
            ))
        else:
            console.print("[yellow]No PwnBox info found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@pwnbox.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_pwnbox():
    """Get PwnBox list"""
    try:
        api_client = HTBAPIClient()
        pwnbox_module = PwnBoxModule(api_client)
        result = pwnbox_module.get_pwnbox_list()
        
        if result and 'data' in result:
            list_data = result['data']
            
            table = Table(title="PwnBox List")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Region", style="magenta")
            table.add_column("IP", style="blue")
            
            for pwnbox in list_data:
                table.add_row(
                    str(pwnbox.get('id', 'N/A') or 'N/A'),
                    str(pwnbox.get('name', 'N/A') or 'N/A'),
                    str(pwnbox.get('status', 'N/A') or 'N/A'),
                    str(pwnbox.get('region', 'N/A') or 'N/A'),
                    str(pwnbox.get('ip', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No PwnBox list found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@pwnbox.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

def terminals(debug):
    """Get PwnBox terminals"""
    try:
        api_client = HTBAPIClient()
        pwnbox_module = PwnBoxModule(api_client)
        result = pwnbox_module.get_pwnbox_terminals()
        
        if result and 'data' in result:
            terminals_data = result['data']
            
            table = Table(title="PwnBox Terminals")
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

@pwnbox.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

def terminals_list(debug):
    """Get PwnBox terminals list"""
    try:
        api_client = HTBAPIClient()
        pwnbox_module = PwnBoxModule(api_client)
        result = pwnbox_module.get_pwnbox_terminals_list()
        
        if result and 'data' in result:
            terminals_list_data = result['data']
            
            table = Table(title="PwnBox Terminals List")
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
