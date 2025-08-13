"""
Badges module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

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
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def list_badges(debug, json_output):
    """List all badges"""
    try:
        api_client = HTBAPIClient()
        badges_module = BadgesModule(api_client)
        result = badges_module.get_badges()
        
        if handle_debug_option(debug, result, "Debug: Badges API Response", json_output):
            return
        
        if result and 'categories' in result:
            categories_data = result['categories']
            
            table = Table(title="Badge Categories")
            table.add_column("Category", style="cyan")
            table.add_column("Description", style="green")
            table.add_column("Badge Count", style="yellow")
            
            for category in categories_data:
                badge_count = len(category.get('badges', []))
                table.add_row(
                    category.get('name', 'N/A'),
                    category.get('description', 'N/A'),
                    str(badge_count)
                )
            
            console.print(table)
        else:
            console.print("[yellow]No badge categories found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
