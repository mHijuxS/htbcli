"""
Review module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

class ReviewModule:
    """Module for handling product review-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_review_helpful(self, review_id: int) -> Dict[str, Any]:
        """Mark review as helpful"""
        return self.api.post(f"/review/helpful/{review_id}")
    
    def get_review_unhelpful(self, review_id: int) -> Dict[str, Any]:
        """Mark review as unhelpful"""
        return self.api.post(f"/review/unhelpful/{review_id}")

# Click commands
@click.group()
def review():
    """Product review-related commands"""
    pass

@review.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('review_id', type=int)
def helpful(review_id, debug):
    """Mark review as helpful"""
    try:
        api_client = HTBAPIClient()
        review_module = ReviewModule(api_client)
        result = review_module.get_review_helpful(review_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Review Helpful Result[/bold green]\n"
                f"Review ID: {review_id}\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Mark Helpful"
            ))
        else:
            console.print("[yellow]No result from helpful action[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@review.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('review_id', type=int)
def unhelpful(review_id, debug):
    """Mark review as unhelpful"""
    try:
        api_client = HTBAPIClient()
        review_module = ReviewModule(api_client)
        result = review_module.get_review_unhelpful(review_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Review Unhelpful Result[/bold green]\n"
                f"Review ID: {review_id}\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Mark Unhelpful"
            ))
        else:
            console.print("[yellow]No result from unhelpful action[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
