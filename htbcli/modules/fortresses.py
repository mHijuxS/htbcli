"""
Fortresses module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class FortressesModule:
    """Module for handling fortress-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_fortresses(self) -> Dict[str, Any]:
        """Get list of fortresses"""
        return self.api.get("/fortresses")
    
    def get_fortress(self, fortress_id: int) -> Dict[str, Any]:
        """Get fortress profile by ID"""
        return self.api.get(f"/fortress/{fortress_id}")
    
    def submit_fortress_flag(self, fortress_id: int, flag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit flag for fortress"""
        return self.api.post(f"/fortress/{fortress_id}/flag", json_data=flag_data)
    
    def get_fortress_flags(self, fortress_id: int) -> Dict[str, Any]:
        """Get list of flags for fortress"""
        return self.api.get(f"/fortress/{fortress_id}/flags")
    
    def reset_fortress(self, fortress_id: int) -> Dict[str, Any]:
        """Vote reset fortress"""
        return self.api.post(f"/fortress/{fortress_id}/reset")

# Click commands
@click.group()
def fortresses():
    """Fortress-related commands"""
    pass

@fortresses.command()
def list():
    """List fortresses"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.get_fortresses()
        
        if result and 'data' in result:
            fortresses_data = result['data']
            
            table = Table(title="Fortresses")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Name", style="green", no_wrap=True)
            table.add_column("New", style="yellow", no_wrap=True)
            table.add_column("Flags", style="magenta", no_wrap=True)
            
            try:
                # Convert object to list of fortresses
                fortresses_list = []
                for key, value in fortresses_data.items():
                    if isinstance(value, dict):
                        fortresses_list.append(value)
                
                for fortress in fortresses_list:
                    fortress_id = str(fortress.get('id', 'N/A') or 'N/A')
                    fortress_name = str(fortress.get('name', 'N/A') or 'N/A')
                    fortress_new = 'Yes' if fortress.get('new') else 'No'
                    fortress_flags = str(fortress.get('number_of_flags', 'N/A') or 'N/A')
                    
                    table.add_row(fortress_id, fortress_name, fortress_new, fortress_flags)
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing fortresses data: {e}[/yellow]")
                console.print(f"[yellow]Data type: {type(fortresses_data)}[/yellow]")
                console.print(f"[yellow]Data: {fortresses_data}[/yellow]")
        else:
            console.print("[yellow]No fortresses found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@fortresses.command()
@click.argument('fortress_id', type=int)
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def info(fortress_id, responses, option):
    """Get fortress info by ID"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.get_fortress(fortress_id)
        
        if result and 'data' in result:
            fortress_data = result['data']
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Fortress Data[/bold green]\n"
                    f"{fortress_data}",
                    title=f"Fortress ID: {fortress_id}"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Fortress Info[/bold green]\n"
                for field in option:
                    value = fortress_data.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title=f"Fortress ID: {fortress_id}"))
            else:
                # Show default fields
                console.print(Panel.fit(
                    f"[bold green]Fortress Info[/bold green]\n"
                    f"ID: {fortress_data.get('id', 'N/A') or 'N/A'}\n"
                    f"Name: {fortress_data.get('name', 'N/A') or 'N/A'}\n"
                    f"IP: {fortress_data.get('ip', 'N/A') or 'N/A'}\n"
                    f"Points: {fortress_data.get('points', 'N/A') or 'N/A'}\n"
                    f"Progress: {fortress_data.get('progress_percent', 'N/A') or 'N/A'}%\n"
                    f"Players Completed: {fortress_data.get('players_completed', 'N/A') or 'N/A'}\n"
                    f"Description: {fortress_data.get('description', 'N/A') or 'N/A'}",
                    title=f"Fortress ID: {fortress_id}"
                ))
        else:
            console.print("[yellow]Fortress not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@fortresses.command()
@click.argument('fortress_id', type=int)
@click.argument('flag')
def submit_flag(fortress_id, flag):
    """Submit flag for fortress"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        flag_data = {"flag": flag}
        result = fortresses_module.submit_fortress_flag(fortress_id, flag_data)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Flag Submission Result[/bold green]\n"
                f"Fortress ID: {fortress_id}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Fortress Flag Submission"
            ))
        else:
            console.print("[yellow]No result from flag submission[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@fortresses.command()
@click.argument('fortress_id', type=int)
def flags(fortress_id):
    """Get list of flags for fortress"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.get_fortress_flags(fortress_id)
        
        if result and 'data' in result:
            flags_data = result['data']
            
            table = Table(title=f"Fortress Flags (ID: {fortress_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Points", style="yellow")
            table.add_column("Owned", style="magenta")
            
            for flag in flags_data:
                table.add_row(
                    str(flag.get('id', 'N/A') or 'N/A'),
                    str(flag.get('title', 'N/A') or 'N/A'),
                    str(flag.get('points', 'N/A') or 'N/A'),
                    str(flag.get('owned', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No flags found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@fortresses.command()
@click.argument('fortress_id', type=int)
def reset(fortress_id):
    """Vote reset fortress"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.reset_fortress(fortress_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Fortress Reset Result[/bold green]\n"
                f"Fortress ID: {fortress_id}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Fortress Reset"
            ))
        else:
            console.print("[yellow]No result from reset[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
