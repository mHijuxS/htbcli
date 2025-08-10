"""
Season module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class SeasonModule:
    """Module for handling Season/Arena-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_season_activity(self, season_id: int) -> Dict[str, Any]:
        """Get season activity"""
        return self.api.get(f"/season/activity/{season_id}")
    
    def get_season_changelog(self, season_id: int) -> Dict[str, Any]:
        """Get season changelog"""
        return self.api.get(f"/season/changelog/{season_id}")
    
    def get_season_info(self, season_slug: str) -> Dict[str, Any]:
        """Get season info by slug"""
        return self.api.get(f"/season/info/{season_slug}")
    
    def get_season_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of seasons"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/season/list", params=params)
    
    def get_season_recommended(self) -> Dict[str, Any]:
        """Get recommended seasons"""
        return self.api.get("/season/recommended")
    
    def get_season_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired seasons"""
        return self.api.get("/season/recommended/retired")
    
    def submit_season_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit season review"""
        return self.api.post("/season/review", json_data=review_data)
    
    def get_season_reviews_user(self, season_id: int) -> Dict[str, Any]:
        """Get user's review for season"""
        return self.api.get(f"/season/reviews/user/{season_id}")
    
    def get_season_writeup(self, season_id: int) -> Dict[str, Any]:
        """Get season writeup"""
        return self.api.get(f"/season/{season_id}/writeup")
    
    def get_season_writeup_official(self, season_id: int) -> Dict[str, Any]:
        """Get official season writeup"""
        return self.api.get(f"/season/{season_id}/writeup/official")
    
    def get_seasons(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of seasons (alternative endpoint)"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/seasons", params=params)

# Click commands
@click.group()
def season():
    """Season/Arena-related commands"""
    pass

@season.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
def list(page, per_page):
    """List seasons"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_list(page, per_page)
        
        if result and 'data' in result:
            seasons_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Seasons (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Type", style="yellow")
            table.add_column("Status", style="magenta")
            table.add_column("Participants", style="blue")
            table.add_column("Start Date", style="red")
            
            try:
                for season in seasons_data:
                    table.add_row(
                        str(season.get('id', 'N/A') or 'N/A'),
                        str(season.get('name', 'N/A') or 'N/A'),
                        str(season.get('type', 'N/A') or 'N/A'),
                        str(season.get('status', 'N/A') or 'N/A'),
                        str(season.get('participants_count', 'N/A') or 'N/A'),
                        str(season.get('start_date', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing seasons data: {e}[/yellow]")
        else:
            console.print("[yellow]No seasons found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('season_slug')
def info(season_slug):
    """Get season info by slug"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_info(season_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]Season Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Type: {info.get('type', 'N/A') or 'N/A'}\n"
                f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                f"Participants: {info.get('participants_count', 'N/A') or 'N/A'}\n"
                f"Start Date: {info.get('start_date', 'N/A') or 'N/A'}\n"
                f"End Date: {info.get('end_date', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Season: {season_slug}"
            ))
        else:
            console.print("[yellow]Season not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
def recommended():
    """Get recommended seasons"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
            table = Table(title="Recommended Seasons")
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Participants", style="magenta")
            
            for season in recommended_data:
                table.add_row(
                    str(season.get('name', 'N/A') or 'N/A'),
                    str(season.get('type', 'N/A') or 'N/A'),
                    str(season.get('status', 'N/A') or 'N/A'),
                    str(season.get('participants_count', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No recommended seasons found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('season_id', type=int)
def activity(season_id):
    """Get season activity"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_activity(season_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Season Activity (ID: {season_id})")
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

@season.command()
@click.argument('season_id', type=int)
def changelog(season_id):
    """Get season changelog"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_changelog(season_id)
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            table = Table(title=f"Season Changelog (ID: {season_id})")
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

@season.command()
@click.argument('season_id', type=int)
def writeup(season_id):
    """Get season writeup"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_writeup(season_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Season Writeup[/bold green]\n"
                f"Season ID: {season_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Season Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('season_id', type=int)
def writeup_official(season_id):
    """Get official season writeup"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_writeup_official(season_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Official Season Writeup[/bold green]\n"
                f"Season ID: {season_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Official Writeup"
            ))
        else:
            console.print("[yellow]No official writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
