"""
Career module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class CareerModule:
    """Module for handling career-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_career_activity(self, career_id: int) -> Dict[str, Any]:
        """Get career activity"""
        return self.api.get(f"/career/activity/{career_id}")
    
    def get_career_changelog(self, career_id: int) -> Dict[str, Any]:
        """Get career changelog"""
        return self.api.get(f"/career/changelog/{career_id}")
    
    def get_career_info(self, career_slug: str) -> Dict[str, Any]:
        """Get career info by slug"""
        return self.api.get(f"/career/info/{career_slug}")
    
    def get_career_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of careers"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/career/list", params=params)
    
    def get_career_recommended(self) -> Dict[str, Any]:
        """Get recommended careers"""
        return self.api.get("/career/recommended")
    
    def get_career_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired careers"""
        return self.api.get("/career/recommended/retired")
    
    def submit_career_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit career review"""
        return self.api.post("/career/review", json_data=review_data)
    
    def get_career_reviews_user(self, career_id: int) -> Dict[str, Any]:
        """Get user's review for career"""
        return self.api.get(f"/career/reviews/user/{career_id}")
    
    def get_career_writeup(self, career_id: int) -> Dict[str, Any]:
        """Get career writeup"""
        return self.api.get(f"/career/{career_id}/writeup")
    
    def get_career_writeup_official(self, career_id: int) -> Dict[str, Any]:
        """Get official career writeup"""
        return self.api.get(f"/career/{career_id}/writeup/official")

# Click commands
@click.group()
def career():
    """Career-related commands"""
    pass

@career.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
def list(page, per_page):
    """List careers"""
    try:
        api_client = HTBAPIClient()
        career_module = CareerModule(api_client)
        result = career_module.get_career_list(page, per_page)
        
        if result and 'data' in result:
            careers_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Careers (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Category", style="yellow")
            table.add_column("Difficulty", style="magenta")
            table.add_column("Points", style="blue")
            table.add_column("Status", style="red")
            
            try:
                for career in careers_data:
                    table.add_row(
                        str(career.get('id', 'N/A') or 'N/A'),
                        str(career.get('name', 'N/A') or 'N/A'),
                        str(career.get('category', 'N/A') or 'N/A'),
                        str(career.get('difficulty', 'N/A') or 'N/A'),
                        str(career.get('points', 'N/A') or 'N/A'),
                        str(career.get('status', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing careers data: {e}[/yellow]")
        else:
            console.print("[yellow]No careers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@career.command()
@click.argument('career_slug')
def info(career_slug):
    """Get career info by slug"""
    try:
        api_client = HTBAPIClient()
        career_module = CareerModule(api_client)
        result = career_module.get_career_info(career_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]Career Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Category: {info.get('category', 'N/A') or 'N/A'}\n"
                f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}\n"
                f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Career: {career_slug}"
            ))
        else:
            console.print("[yellow]Career not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@career.command()
def recommended():
    """Get recommended careers"""
    try:
        api_client = HTBAPIClient()
        career_module = CareerModule(api_client)
        result = career_module.get_career_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
            table = Table(title="Recommended Careers")
            table.add_column("Name", style="cyan")
            table.add_column("Category", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Points", style="magenta")
            
            for career in recommended_data:
                table.add_row(
                    str(career.get('name', 'N/A') or 'N/A'),
                    str(career.get('category', 'N/A') or 'N/A'),
                    str(career.get('difficulty', 'N/A') or 'N/A'),
                    str(career.get('points', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No recommended careers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@career.command()
@click.argument('career_id', type=int)
def activity(career_id):
    """Get career activity"""
    try:
        api_client = HTBAPIClient()
        career_module = CareerModule(api_client)
        result = career_module.get_career_activity(career_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Career Activity (ID: {career_id})")
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

@career.command()
@click.argument('career_id', type=int)
def changelog(career_id):
    """Get career changelog"""
    try:
        api_client = HTBAPIClient()
        career_module = CareerModule(api_client)
        result = career_module.get_career_changelog(career_id)
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            table = Table(title=f"Career Changelog (ID: {career_id})")
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

@career.command()
@click.argument('career_id', type=int)
def writeup(career_id):
    """Get career writeup"""
    try:
        api_client = HTBAPIClient()
        career_module = CareerModule(api_client)
        result = career_module.get_career_writeup(career_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Career Writeup[/bold green]\n"
                f"Career ID: {career_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Career Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@career.command()
@click.argument('career_id', type=int)
def writeup_official(career_id):
    """Get official career writeup"""
    try:
        api_client = HTBAPIClient()
        career_module = CareerModule(api_client)
        result = career_module.get_career_writeup_official(career_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Official Career Writeup[/bold green]\n"
                f"Career ID: {career_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Official Writeup"
            ))
        else:
            console.print("[yellow]No official writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
