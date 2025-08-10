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
    
    def get_fortress_activity(self, fortress_id: int) -> Dict[str, Any]:
        """Get fortress activity"""
        return self.api.get(f"/fortress/activity/{fortress_id}")
    
    def get_fortress_info(self, fortress_slug: str) -> Dict[str, Any]:
        """Get fortress info by slug"""
        return self.api.get(f"/fortress/info/{fortress_slug}")
    
    def get_fortress_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of fortresses"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/fortress/list", params=params)
    
    def get_fortress_recommended(self) -> Dict[str, Any]:
        """Get recommended fortresses"""
        return self.api.get("/fortress/recommended")
    
    def get_fortress_writeup(self, fortress_id: int) -> Dict[str, Any]:
        """Get fortress writeup"""
        return self.api.get(f"/fortress/{fortress_id}/writeup")

# Click commands
@click.group()
def fortresses():
    """Fortress-related commands"""
    pass

@fortresses.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
def list(page, per_page):
    """List fortresses"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.get_fortress_list(page, per_page)
        
        if result and 'data' in result:
            fortresses_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Fortresses (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Points", style="magenta")
            table.add_column("Status", style="blue")
            table.add_column("Machines", style="red")
            
            try:
                for fortress in fortresses_data:
                    table.add_row(
                        str(fortress.get('id', 'N/A') or 'N/A'),
                        str(fortress.get('name', 'N/A') or 'N/A'),
                        str(fortress.get('difficulty', 'N/A') or 'N/A'),
                        str(fortress.get('points', 'N/A') or 'N/A'),
                        str(fortress.get('status', 'N/A') or 'N/A'),
                        str(fortress.get('machines_count', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing fortresses data: {e}[/yellow]")
        else:
            console.print("[yellow]No fortresses found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@fortresses.command()
@click.argument('fortress_slug')
def info(fortress_slug):
    """Get fortress info by slug"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.get_fortress_info(fortress_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]Fortress Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}\n"
                f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                f"Machines: {info.get('machines_count', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Fortress: {fortress_slug}"
            ))
        else:
            console.print("[yellow]Fortress not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@fortresses.command()
def recommended():
    """Get recommended fortresses"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.get_fortress_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
            table = Table(title="Recommended Fortresses")
            table.add_column("Name", style="cyan")
            table.add_column("Difficulty", style="green")
            table.add_column("Points", style="yellow")
            table.add_column("Machines", style="magenta")
            
            for fortress in recommended_data:
                table.add_row(
                    str(fortress.get('name', 'N/A') or 'N/A'),
                    str(fortress.get('difficulty', 'N/A') or 'N/A'),
                    str(fortress.get('points', 'N/A') or 'N/A'),
                    str(fortress.get('machines_count', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No recommended fortresses found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@fortresses.command()
@click.argument('fortress_id', type=int)
def activity(fortress_id):
    """Get fortress activity"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.get_fortress_activity(fortress_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Fortress Activity (ID: {fortress_id})")
            table.add_column("User", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Date", style="yellow")
            table.add_column("Points", style="magenta")
            
            for activity in activity_data:
                table.add_row(
                    str(activity.get('user', 'N/A') or 'N/A'),
                    str(activity.get('type', 'N/A') or 'N/A'),
                    str(activity.get('date', 'N/A') or 'N/A'),
                    str(activity.get('points', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No activity found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@fortresses.command()
@click.argument('fortress_id', type=int)
def writeup(fortress_id):
    """Get fortress writeup"""
    try:
        api_client = HTBAPIClient()
        fortresses_module = FortressesModule(api_client)
        result = fortresses_module.get_fortress_writeup(fortress_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Fortress Writeup[/bold green]\n"
                f"Fortress ID: {fortress_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Fortress Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
