"""
Ranking module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class RankingModule:
    """Module for handling ranking-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_ranking_activity(self, ranking_id: int) -> Dict[str, Any]:
        """Get ranking activity"""
        return self.api.get(f"/ranking/activity/{ranking_id}")
    
    def get_ranking_changelog(self, ranking_id: int) -> Dict[str, Any]:
        """Get ranking changelog"""
        return self.api.get(f"/ranking/changelog/{ranking_id}")
    
    def get_ranking_info(self, ranking_slug: str) -> Dict[str, Any]:
        """Get ranking info by slug"""
        return self.api.get(f"/ranking/info/{ranking_slug}")
    
    def get_ranking_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of rankings"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/ranking/list", params=params)
    
    def get_ranking_recommended(self) -> Dict[str, Any]:
        """Get recommended rankings"""
        return self.api.get("/ranking/recommended")
    
    def get_ranking_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired rankings"""
        return self.api.get("/ranking/recommended/retired")
    
    def submit_ranking_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit ranking review"""
        return self.api.post("/ranking/review", json_data=review_data)
    
    def get_ranking_reviews_user(self, ranking_id: int) -> Dict[str, Any]:
        """Get user's review for ranking"""
        return self.api.get(f"/ranking/reviews/user/{ranking_id}")
    
    def get_ranking_writeup(self, ranking_id: int) -> Dict[str, Any]:
        """Get ranking writeup"""
        return self.api.get(f"/ranking/{ranking_id}/writeup")
    
    def get_ranking_writeup_official(self, ranking_id: int) -> Dict[str, Any]:
        """Get official ranking writeup"""
        return self.api.get(f"/ranking/{ranking_id}/writeup/official")
    
    def get_rankings(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of rankings (alternative endpoint)"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/rankings", params=params)
    
    def get_rankings_info(self, ranking_slug: str) -> Dict[str, Any]:
        """Get ranking info by slug (alternative endpoint)"""
        return self.api.get(f"/rankings/info/{ranking_slug}")
    
    def get_rankings_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of rankings (alternative endpoint)"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/rankings/list", params=params)
    
    def get_rankings_activity(self, ranking_id: int) -> Dict[str, Any]:
        """Get ranking activity (alternative endpoint)"""
        return self.api.get(f"/rankings/activity/{ranking_id}")
    
    def get_rankings_changelog(self, ranking_id: int) -> Dict[str, Any]:
        """Get ranking changelog (alternative endpoint)"""
        return self.api.get(f"/rankings/changelog/{ranking_id}")
    
    def get_rankings_recommended(self) -> Dict[str, Any]:
        """Get recommended rankings (alternative endpoint)"""
        return self.api.get("/rankings/recommended")
    
    def get_rankings_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired rankings (alternative endpoint)"""
        return self.api.get("/rankings/recommended/retired")
    
    def get_rankings_writeup(self, ranking_id: int) -> Dict[str, Any]:
        """Get ranking writeup (alternative endpoint)"""
        return self.api.get(f"/rankings/{ranking_id}/writeup")
    
    def get_rankings_writeup_official(self, ranking_id: int) -> Dict[str, Any]:
        """Get official ranking writeup (alternative endpoint)"""
        return self.api.get(f"/rankings/{ranking_id}/writeup/official")

# Click commands
@click.group()
def ranking():
    """Ranking-related commands"""
    pass

@ranking.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_ranking(page, per_page):
    """List rankings"""
    try:
        api_client = HTBAPIClient()
        ranking_module = RankingModule(api_client)
        result = ranking_module.get_ranking_list(page, per_page)
        
        if result and 'data' in result:
            rankings_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Rankings (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Type", style="yellow")
            table.add_column("Status", style="magenta")
            table.add_column("Participants", style="blue")
            table.add_column("Start Date", style="red")
            
            try:
                for ranking in rankings_data:
                    table.add_row(
                        str(ranking.get('id', 'N/A') or 'N/A'),
                        str(ranking.get('name', 'N/A') or 'N/A'),
                        str(ranking.get('type', 'N/A') or 'N/A'),
                        str(ranking.get('status', 'N/A') or 'N/A'),
                        str(ranking.get('participants_count', 'N/A') or 'N/A'),
                        str(ranking.get('start_date', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing rankings data: {e}[/yellow]")
        else:
            console.print("[yellow]No rankings found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@ranking.command()
@click.argument('ranking_slug')
def info(ranking_slug):
    """Get ranking info by slug"""
    try:
        api_client = HTBAPIClient()
        ranking_module = RankingModule(api_client)
        result = ranking_module.get_ranking_info(ranking_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]Ranking Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Type: {info.get('type', 'N/A') or 'N/A'}\n"
                f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                f"Participants: {info.get('participants_count', 'N/A') or 'N/A'}\n"
                f"Start Date: {info.get('start_date', 'N/A') or 'N/A'}\n"
                f"End Date: {info.get('end_date', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Ranking: {ranking_slug}"
            ))
        else:
            console.print("[yellow]Ranking not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@ranking.command()
def recommended():
    """Get recommended rankings"""
    try:
        api_client = HTBAPIClient()
        ranking_module = RankingModule(api_client)
        result = ranking_module.get_ranking_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
            table = Table(title="Recommended Rankings")
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Participants", style="magenta")
            
            for ranking in recommended_data:
                table.add_row(
                    str(ranking.get('name', 'N/A') or 'N/A'),
                    str(ranking.get('type', 'N/A') or 'N/A'),
                    str(ranking.get('status', 'N/A') or 'N/A'),
                    str(ranking.get('participants_count', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No recommended rankings found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@ranking.command()
@click.argument('ranking_id', type=int)
def activity(ranking_id):
    """Get ranking activity"""
    try:
        api_client = HTBAPIClient()
        ranking_module = RankingModule(api_client)
        result = ranking_module.get_ranking_activity(ranking_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Ranking Activity (ID: {ranking_id})")
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

@ranking.command()
@click.argument('ranking_id', type=int)
def changelog(ranking_id):
    """Get ranking changelog"""
    try:
        api_client = HTBAPIClient()
        ranking_module = RankingModule(api_client)
        result = ranking_module.get_ranking_changelog(ranking_id)
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            table = Table(title=f"Ranking Changelog (ID: {ranking_id})")
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

@ranking.command()
@click.argument('ranking_id', type=int)
def writeup(ranking_id):
    """Get ranking writeup"""
    try:
        api_client = HTBAPIClient()
        ranking_module = RankingModule(api_client)
        result = ranking_module.get_ranking_writeup(ranking_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Ranking Writeup[/bold green]\n"
                f"Ranking ID: {ranking_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Ranking Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@ranking.command()
@click.argument('ranking_id', type=int)
def writeup_official(ranking_id):
    """Get official ranking writeup"""
    try:
        api_client = HTBAPIClient()
        ranking_module = RankingModule(api_client)
        result = ranking_module.get_ranking_writeup_official(ranking_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Official Ranking Writeup[/bold green]\n"
                f"Ranking ID: {ranking_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Official Writeup"
            ))
        else:
            console.print("[yellow]No official writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
