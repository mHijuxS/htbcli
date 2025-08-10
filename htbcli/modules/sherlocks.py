"""
Sherlocks module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class SherlocksModule:
    """Module for handling Sherlock-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_sherlock_activity(self, sherlock_id: int) -> Dict[str, Any]:
        """Get sherlock activity"""
        return self.api.get(f"/sherlock/activity/{sherlock_id}")
    
    def get_sherlock_changelog(self, sherlock_id: int) -> Dict[str, Any]:
        """Get sherlock changelog"""
        return self.api.get(f"/sherlock/changelog/{sherlock_id}")
    
    def get_sherlock_info(self, sherlock_slug: str) -> Dict[str, Any]:
        """Get sherlock info by slug"""
        return self.api.get(f"/sherlock/info/{sherlock_slug}")
    
    def get_sherlock_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of sherlocks"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/sherlock/list", params=params)
    
    def get_sherlock_recommended(self) -> Dict[str, Any]:
        """Get recommended sherlocks"""
        return self.api.get("/sherlock/recommended")
    
    def get_sherlock_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired sherlocks"""
        return self.api.get("/sherlock/recommended/retired")
    
    def submit_sherlock_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit sherlock review"""
        return self.api.post("/sherlock/review", json_data=review_data)
    
    def get_sherlock_reviews_user(self, sherlock_id: int) -> Dict[str, Any]:
        """Get user's review for sherlock"""
        return self.api.get(f"/sherlock/reviews/user/{sherlock_id}")
    
    def get_sherlock_writeup(self, sherlock_id: int) -> Dict[str, Any]:
        """Get sherlock writeup"""
        return self.api.get(f"/sherlock/{sherlock_id}/writeup")
    
    def get_sherlock_writeup_official(self, sherlock_id: int) -> Dict[str, Any]:
        """Get official sherlock writeup"""
        return self.api.get(f"/sherlock/{sherlock_id}/writeup/official")
    
    def get_sherlocks(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of sherlocks (alternative endpoint)"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/sherlocks", params=params)
    
    def get_sherlocks_info(self, sherlock_slug: str) -> Dict[str, Any]:
        """Get sherlock info by slug (alternative endpoint)"""
        return self.api.get(f"/sherlocks/info/{sherlock_slug}")

# Click commands
@click.group()
def sherlocks():
    """Sherlock-related commands"""
    pass

@sherlocks.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_sherlocks(page, per_page):
    """List sherlocks"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_list(page, per_page)
        
        if result and 'data' in result:
            sherlocks_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Sherlocks (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Category", style="yellow")
            table.add_column("Difficulty", style="magenta")
            table.add_column("Points", style="blue")
            table.add_column("Status", style="red")
            
            try:
                for sherlock in sherlocks_data:
                    table.add_row(
                        str(sherlock.get('id', 'N/A') or 'N/A'),
                        str(sherlock.get('name', 'N/A') or 'N/A'),
                        str(sherlock.get('category', 'N/A') or 'N/A'),
                        str(sherlock.get('difficulty', 'N/A') or 'N/A'),
                        str(sherlock.get('points', 'N/A') or 'N/A'),
                        str(sherlock.get('status', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing sherlocks data: {e}[/yellow]")
        else:
            console.print("[yellow]No sherlocks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_slug')
def info(sherlock_slug):
    """Get sherlock info by slug"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_info(sherlock_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]Sherlock Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Category: {info.get('category', 'N/A') or 'N/A'}\n"
                f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}\n"
                f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Sherlock: {sherlock_slug}"
            ))
        else:
            console.print("[yellow]Sherlock not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
def recommended():
    """Get recommended sherlocks"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
            table = Table(title="Recommended Sherlocks")
            table.add_column("Name", style="cyan")
            table.add_column("Category", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Points", style="magenta")
            
            for sherlock in recommended_data:
                table.add_row(
                    str(sherlock.get('name', 'N/A') or 'N/A'),
                    str(sherlock.get('category', 'N/A') or 'N/A'),
                    str(sherlock.get('difficulty', 'N/A') or 'N/A'),
                    str(sherlock.get('points', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No recommended sherlocks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def activity(sherlock_id):
    """Get sherlock activity"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_activity(sherlock_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Sherlock Activity (ID: {sherlock_id})")
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

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def changelog(sherlock_id):
    """Get sherlock changelog"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_changelog(sherlock_id)
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            table = Table(title=f"Sherlock Changelog (ID: {sherlock_id})")
            table.add_column("Date", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Description", style="yellow")
            
            for change in changelog_data:
                table.add_row(
                    str(change.get('date', 'N/A') or 'N/A'),
                    str(change.get('type', 'N/A') or 'N/A'),
                    str(change.get('description', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No changelog found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def writeup(sherlock_id):
    """Get sherlock writeup"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_writeup(sherlock_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Sherlock Writeup[/bold green]\n"
                f"Sherlock ID: {sherlock_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Sherlock Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def writeup_official(sherlock_id):
    """Get official sherlock writeup"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_writeup_official(sherlock_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Official Sherlock Writeup[/bold green]\n"
                f"Sherlock ID: {sherlock_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Official Writeup"
            ))
        else:
            console.print("[yellow]No official writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
