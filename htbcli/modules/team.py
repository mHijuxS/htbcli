"""
Team module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class TeamModule:
    """Module for handling team ranking-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_team_activity(self, team_id: int) -> Dict[str, Any]:
        """Get team activity"""
        return self.api.get(f"/team/activity/{team_id}")
    
    def get_team_changelog(self, team_id: int) -> Dict[str, Any]:
        """Get team changelog"""
        return self.api.get(f"/team/changelog/{team_id}")
    
    def get_team_info(self, team_slug: str) -> Dict[str, Any]:
        """Get team info by slug"""
        return self.api.get(f"/team/info/{team_slug}")
    
    def get_team_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of teams"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/team/list", params=params)
    
    def get_team_recommended(self) -> Dict[str, Any]:
        """Get recommended teams"""
        return self.api.get("/team/recommended")
    
    def get_team_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired teams"""
        return self.api.get("/team/recommended/retired")
    
    def submit_team_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit team review"""
        return self.api.post("/team/review", json_data=review_data)
    
    def get_team_reviews_user(self, team_id: int) -> Dict[str, Any]:
        """Get user's review for team"""
        return self.api.get(f"/team/reviews/user/{team_id}")
    
    def get_team_writeup(self, team_id: int) -> Dict[str, Any]:
        """Get team writeup"""
        return self.api.get(f"/team/{team_id}/writeup")
    
    def get_team_writeup_official(self, team_id: int) -> Dict[str, Any]:
        """Get official team writeup"""
        return self.api.get(f"/team/{team_id}/writeup/official")
    
    def get_teams(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of teams (alternative endpoint)"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/teams", params=params)

# Click commands
@click.group()
def team():
    """Team ranking-related commands"""
    pass

@team.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_team(page, per_page, responses, option):
    """List teams"""
    try:
        api_client = HTBAPIClient()
        team_module = TeamModule(api_client)
        result = team_module.get_team_list(page, per_page)
        
        if result and 'data' in result:
            teams_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            if responses:
                # Show all available fields for first team
                if teams_data:
                    first_team = teams_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Teams[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_team.items()])}",
                        title=f"Teams - All Fields (First Item, Page {page})"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title=f"Teams - Selected Fields (Page {page})")
                table.add_column("ID", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for team in teams_data:
                    row = [str(team.get('id', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(team.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title=f"Teams (Page {page})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Type", style="yellow")
                table.add_column("Status", style="magenta")
                table.add_column("Members", style="blue")
                table.add_column("Points", style="red")
                
                try:
                    for team in teams_data:
                        table.add_row(
                            str(team.get('id', 'N/A') or 'N/A'),
                            str(team.get('name', 'N/A') or 'N/A'),
                            str(team.get('type', 'N/A') or 'N/A'),
                            str(team.get('status', 'N/A') or 'N/A'),
                            str(team.get('members_count', 'N/A') or 'N/A'),
                            str(team.get('points', 'N/A') or 'N/A')
                        )
                    
                    console.print(table)
                except Exception as e:
                    console.print(f"[yellow]Error processing teams data: {e}[/yellow]")
        else:
            console.print("[yellow]No teams found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@team.command()
@click.argument('team_slug')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def info(team_slug, responses, option):
    """Get team info by slug"""
    try:
        api_client = HTBAPIClient()
        team_module = TeamModule(api_client)
        result = team_module.get_team_info(team_slug)
        
        if result and 'info' in result:
            info = result['info']
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for Team Info[/bold green]\n"
                    f"{chr(10).join([f'{k}: {v}' for k, v in info.items()])}",
                    title=f"Team: {team_slug} - All Fields"
                ))
            elif option:
                # Show only specified fields
                selected_info = {}
                for field in option:
                    if field in info:
                        selected_info[field] = info[field]
                    else:
                        console.print(f"[yellow]Field '{field}' not found in response[/yellow]")
                
                if selected_info:
                    console.print(Panel.fit(
                        f"[bold green]Selected Fields[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in selected_info.items()])}",
                        title=f"Team: {team_slug} - Selected Fields"
                    ))
            else:
                # Default view
                console.print(Panel.fit(
                    f"[bold green]Team Info[/bold green]\n"
                    f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                    f"Type: {info.get('type', 'N/A') or 'N/A'}\n"
                    f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                    f"Members: {info.get('members_count', 'N/A') or 'N/A'}\n"
                    f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                    f"Description: {info.get('description', 'N/A') or 'N/A'}",
                    title=f"Team: {team_slug}"
                ))
        else:
            console.print("[yellow]Team not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@team.command()
def recommended():
    """Get recommended teams"""
    try:
        api_client = HTBAPIClient()
        team_module = TeamModule(api_client)
        result = team_module.get_team_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
            table = Table(title="Recommended Teams")
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Members", style="magenta")
            
            for team in recommended_data:
                table.add_row(
                    str(team.get('name', 'N/A') or 'N/A'),
                    str(team.get('type', 'N/A') or 'N/A'),
                    str(team.get('status', 'N/A') or 'N/A'),
                    str(team.get('members_count', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No recommended teams found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@team.command()
@click.argument('team_id', type=int)
def activity(team_id):
    """Get team activity"""
    try:
        api_client = HTBAPIClient()
        team_module = TeamModule(api_client)
        result = team_module.get_team_activity(team_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Team Activity (ID: {team_id})")
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

@team.command()
@click.argument('team_id', type=int)
def changelog(team_id):
    """Get team changelog"""
    try:
        api_client = HTBAPIClient()
        team_module = TeamModule(api_client)
        result = team_module.get_team_changelog(team_id)
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            table = Table(title=f"Team Changelog (ID: {team_id})")
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

@team.command()
@click.argument('team_id', type=int)
def writeup(team_id):
    """Get team writeup"""
    try:
        api_client = HTBAPIClient()
        team_module = TeamModule(api_client)
        result = team_module.get_team_writeup(team_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Team Writeup[/bold green]\n"
                f"Team ID: {team_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Team Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@team.command()
@click.argument('team_id', type=int)
def writeup_official(team_id):
    """Get official team writeup"""
    try:
        api_client = HTBAPIClient()
        team_module = TeamModule(api_client)
        result = team_module.get_team_writeup_official(team_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Official Team Writeup[/bold green]\n"
                f"Team ID: {team_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Official Writeup"
            ))
        else:
            console.print("[yellow]No official writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
