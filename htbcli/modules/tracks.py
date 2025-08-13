"""
Tracks module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

class TracksModule:
    """Module for handling track-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_track_activity(self, track_id: int) -> Dict[str, Any]:
        """Get track activity"""
        return self.api.get(f"/track/activity/{track_id}")
    
    def get_track_info(self, track_slug: str) -> Dict[str, Any]:
        """Get track info by slug"""
        return self.api.get(f"/track/info/{track_slug}")
    
    def get_track_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of tracks"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/track/list", params=params)
    
    def get_track_writeup(self, track_id: int) -> Dict[str, Any]:
        """Get track writeup"""
        return self.api.get(f"/track/{track_id}/writeup")

# Click commands
@click.group()
def tracks():
    """Track-related commands"""
    pass

@tracks.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_tracks(page, per_page):
    """List tracks"""
    try:
        api_client = HTBAPIClient()
        tracks_module = TracksModule(api_client)
        result = tracks_module.get_track_list(page, per_page)
        
        if result and 'data' in result:
            tracks_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Tracks (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Points", style="magenta")
            table.add_column("Status", style="blue")
            table.add_column("Modules", style="red")
            
            try:
                for track in tracks_data:
                    table.add_row(
                        str(track.get('id', 'N/A') or 'N/A'),
                        str(track.get('name', 'N/A') or 'N/A'),
                        str(track.get('difficulty', 'N/A') or 'N/A'),
                        str(track.get('points', 'N/A') or 'N/A'),
                        str(track.get('status', 'N/A') or 'N/A'),
                        str(track.get('modules_count', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing tracks data: {e}[/yellow]")
        else:
            console.print("[yellow]No tracks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@tracks.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('track_slug')
def info(track_slug, debug):
    """Get track info by slug"""
    try:
        api_client = HTBAPIClient()
        tracks_module = TracksModule(api_client)
        result = tracks_module.get_track_info(track_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]Track Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}\n"
                f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                f"Status: {info.get('status', 'N/A') or 'N/A'}\n"
                f"Modules: {info.get('modules_count', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Track: {track_slug}"
            ))
        else:
            console.print("[yellow]Track not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@tracks.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('track_id', type=int)
def activity(track_id, debug):
    """Get track activity"""
    try:
        api_client = HTBAPIClient()
        tracks_module = TracksModule(api_client)
        result = tracks_module.get_track_activity(track_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Track Activity (ID: {track_id})")
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

@tracks.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('track_id', type=int)
def writeup(track_id, debug):
    """Get track writeup"""
    try:
        api_client = HTBAPIClient()
        tracks_module = TracksModule(api_client)
        result = tracks_module.get_track_writeup(track_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Track Writeup[/bold green]\n"
                f"Track ID: {track_id}\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title="Track Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
