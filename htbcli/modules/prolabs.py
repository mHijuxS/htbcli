"""
Prolabs module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class ProlabsModule:
    """Module for handling ProLab-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_prolab_activity(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab activity"""
        return self.api.get(f"/prolab/activity/{prolab_id}")
    
    def get_prolab_changelog(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab changelog"""
        return self.api.get(f"/prolab/changelog/{prolab_id}")
    
    def get_prolab_info(self, prolab_slug: str) -> Dict[str, Any]:
        """Get prolab info by slug"""
        return self.api.get(f"/prolab/info/{prolab_slug}")
    
    def get_prolab_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of prolabs"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/prolab/list", params=params)
    
    def get_prolab_recommended(self) -> Dict[str, Any]:
        """Get recommended prolabs"""
        return self.api.get("/prolab/recommended")
    
    def get_prolab_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired prolabs"""
        return self.api.get("/prolab/recommended/retired")
    
    def submit_prolab_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit prolab review"""
        return self.api.post("/prolab/review", json_data=review_data)
    
    def get_prolab_reviews_user(self, prolab_id: int) -> Dict[str, Any]:
        """Get user's review for prolab"""
        return self.api.get(f"/prolab/reviews/user/{prolab_id}")
    
    def get_prolab_writeup(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab writeup"""
        return self.api.get(f"/prolab/{prolab_id}/writeup")
    
    def get_prolab_writeup_official(self, prolab_id: int) -> Dict[str, Any]:
        """Get official prolab writeup"""
        return self.api.get(f"/prolab/{prolab_id}/writeup/official")
    
    def get_prolabs(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of prolabs (alternative endpoint)"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/prolabs", params=params)
    
    def get_prolabs_info(self, prolab_slug: str) -> Dict[str, Any]:
        """Get prolab info by slug (alternative endpoint)"""
        return self.api.get(f"/prolabs/info/{prolab_slug}")
    
    def get_prolabs_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of prolabs (alternative endpoint)"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/prolabs/list", params=params)

# Click commands
@click.group()
def prolabs():
    """ProLab-related commands"""
    pass

@prolabs.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
def list(page, per_page):
    """List prolabs"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        result = prolabs_module.get_prolab_list(page, per_page)
        
        if result and 'data' in result:
            prolabs_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"ProLabs (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Points", style="magenta")
            table.add_column("Status", style="blue")
            table.add_column("Machines", style="red")
            
            try:
                for prolab in prolabs_data:
                    table.add_row(
                        str(prolab.get('id', 'N/A') or 'N/A'),
                        str(prolab.get('name', 'N/A') or 'N/A'),
                        str(prolab.get('difficulty', 'N/A') or 'N/A'),
                        str(prolab.get('points', 'N/A') or 'N/A'),
                        str(prolab.get('status', 'N/A') or 'N/A'),
                        str(prolab.get('machines_count', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing prolabs data: {e}[/yellow]")
        else:
            console.print("[yellow]No prolabs found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_slug')
def info(prolab_slug):
    """Get prolab info by slug"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        result = prolabs_module.get_prolab_info(prolab_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]ProLab Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}\n"
                f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                f"Machines: {info.get('machines_count', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"ProLab: {prolab_slug}"
            ))
        else:
            console.print("[yellow]ProLab not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
def recommended():
    """Get recommended prolabs"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        result = prolabs_module.get_prolab_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
            table = Table(title="Recommended ProLabs")
            table.add_column("Name", style="cyan")
            table.add_column("Difficulty", style="green")
            table.add_column("Points", style="yellow")
            table.add_column("Machines", style="magenta")
            
            for prolab in recommended_data:
                table.add_row(
                    str(prolab.get('name', 'N/A') or 'N/A'),
                    str(prolab.get('difficulty', 'N/A') or 'N/A'),
                    str(prolab.get('points', 'N/A') or 'N/A'),
                    str(prolab.get('machines_count', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No recommended prolabs found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_id', type=int)
def activity(prolab_id):
    """Get prolab activity"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        result = prolabs_module.get_prolab_activity(prolab_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"ProLab Activity (ID: {prolab_id})")
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

@prolabs.command()
@click.argument('prolab_id', type=int)
def changelog(prolab_id):
    """Get prolab changelog"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        result = prolabs_module.get_prolab_changelog(prolab_id)
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            table = Table(title=f"ProLab Changelog (ID: {prolab_id})")
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

@prolabs.command()
@click.argument('prolab_id', type=int)
def writeup(prolab_id):
    """Get prolab writeup"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        result = prolabs_module.get_prolab_writeup(prolab_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]ProLab Writeup[/bold green]\n"
                f"ProLab ID: {prolab_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="ProLab Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_id', type=int)
def writeup_official(prolab_id):
    """Get official prolab writeup"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        result = prolabs_module.get_prolab_writeup_official(prolab_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Official ProLab Writeup[/bold green]\n"
                f"ProLab ID: {prolab_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Official Writeup"
            ))
        else:
            console.print("[yellow]No official writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
