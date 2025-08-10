"""
Badges module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class BadgesModule:
    """Module for handling badge-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_badges(self) -> Dict[str, Any]:
        """Get all badges"""
        return self.api.get("/badges")

# Click commands
@click.group()
def badges():
    """Badge-related commands"""
    pass

@badges.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_badges():
    """List all badges"""
    try:
        api_client = HTBAPIClient()
        badges_module = BadgesModule(api_client)
        result = badges_module.get_badges()
        
        if result and 'data' in result:
            badges_data = result['data']
            
            table = Table(title="Badges")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Description", style="yellow")
            table.add_column("Icon", style="magenta")
            
            for badge in badges_data:
                table.add_row(
                    str(badge.get('id', 'N/A')),
                    badge.get('name', 'N/A'),
                    badge.get('description', 'N/A'),
                    badge.get('icon', 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No badges found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
