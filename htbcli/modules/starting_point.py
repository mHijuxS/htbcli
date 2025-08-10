"""
Starting Point module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class StartingPointModule:
    """Module for handling Starting Point-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_starting_point_activity(self, starting_point_id: int) -> Dict[str, Any]:
        """Get starting point activity"""
        return self.api.get(f"/starting-point/activity/{starting_point_id}")
    
    def get_starting_point_info(self, starting_point_slug: str) -> Dict[str, Any]:
        """Get starting point info by slug"""
        return self.api.get(f"/starting-point/info/{starting_point_slug}")
    
    def get_starting_point_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of starting points"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/starting-point/list", params=params)
    
    def get_starting_point_writeup(self, starting_point_id: int) -> Dict[str, Any]:
        """Get starting point writeup"""
        return self.api.get(f"/starting-point/{starting_point_id}/writeup")

# Click commands
@click.group()
def starting_point():
    """Starting Point-related commands"""
    pass

@starting_point.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_starting_point(page, per_page):
    """List starting points"""
    try:
        api_client = HTBAPIClient()
        starting_point_module = StartingPointModule(api_client)
        result = starting_point_module.get_starting_point_list(page, per_page)
        
        if result and 'data' in result:
            starting_points_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Starting Points (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Points", style="magenta")
            table.add_column("Status", style="blue")
            table.add_column("Category", style="red")
            
            try:
                for starting_point in starting_points_data:
                    table.add_row(
                        str(starting_point.get('id', 'N/A') or 'N/A'),
                        str(starting_point.get('name', 'N/A') or 'N/A'),
                        str(starting_point.get('difficulty', 'N/A') or 'N/A'),
                        str(starting_point.get('points', 'N/A') or 'N/A'),
                        str(starting_point.get('status', 'N/A') or 'N/A'),
                        str(starting_point.get('category', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing starting points data: {e}[/yellow]")
        else:
            console.print("[yellow]No starting points found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@starting_point.command()
@click.argument('starting_point_slug')
def info(starting_point_slug):
    """Get starting point info by slug"""
    try:
        api_client = HTBAPIClient()
        starting_point_module = StartingPointModule(api_client)
        result = starting_point_module.get_starting_point_info(starting_point_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]Starting Point Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}\n"
                f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                f"Category: {info.get('category', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Starting Point: {starting_point_slug}"
            ))
        else:
            console.print("[yellow]Starting point not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@starting_point.command()
@click.argument('starting_point_id', type=int)
def activity(starting_point_id):
    """Get starting point activity"""
    try:
        api_client = HTBAPIClient()
        starting_point_module = StartingPointModule(api_client)
        result = starting_point_module.get_starting_point_activity(starting_point_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Starting Point Activity (ID: {starting_point_id})")
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

@starting_point.command()
@click.argument('starting_point_id', type=int)
def writeup(starting_point_id):
    """Get starting point writeup"""
    try:
        api_client = HTBAPIClient()
        starting_point_module = StartingPointModule(api_client)
        result = starting_point_module.get_starting_point_writeup(starting_point_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Starting Point Writeup[/bold green]\n"
                f"Starting Point ID: {starting_point_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Starting Point Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
