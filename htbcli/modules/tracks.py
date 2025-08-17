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
    

    
    def get_track_info(self, track_id: int) -> Dict[str, Any]:
        """Get track info by ID"""
        return self.api.get(f"/tracks/{track_id}")
    
    def get_track_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of tracks"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/tracks", params=params)
    
    def get_track_writeup(self, track_id: int) -> Dict[str, Any]:
        """Get track writeup"""
        return self.api.get(f"/tracks/{track_id}/writeup")
    
    def find_track_id_by_name(self, track_name: str) -> Optional[int]:
        """Find track ID by name"""
        try:
            tracks = self.get_track_list()
            if tracks:
                for track in tracks:
                    if track.get('name', '').lower() == track_name.lower():
                        return track.get('id')
            return None
        except Exception:
            return None
    
    def get_track_items(self, track_id: int) -> Dict[str, Any]:
        """Get track items (machines and challenges)"""
        return self.api.get(f"/tracks/{track_id}")

# Click commands
@click.group()
def tracks():
    """Track-related commands"""
    pass

@tracks.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Items per page')
def list_tracks(responses, option, page, per_page):
    """List tracks"""
    try:
        api_client = HTBAPIClient()
        tracks_module = TracksModule(api_client)
        result = tracks_module.get_track_list(page, per_page)
        
        if result:
            tracks_data = result if isinstance(result, list) else (result.get('data', []) if isinstance(result, dict) else [])
            
            table = Table(title=f"Tracks (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Creator", style="magenta")
            table.add_column("Official", style="blue")
            table.add_column("Likes", style="red")
            
            try:
                for track in tracks_data:
                    table.add_row(
                        str(track.get('id', 'N/A') or 'N/A'),
                        str(track.get('name', 'N/A') or 'N/A'),
                        str(track.get('difficulty', 'N/A') or 'N/A'),
                        str(track.get('creator', {}).get('name', 'N/A') or 'N/A'),
                        str(track.get('official', 'N/A') or 'N/A'),
                        str(track.get('likes', 'N/A') or 'N/A')
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
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('track_identifier')
def info(track_identifier, debug, json_output):
    """Get track info by ID or name"""
    try:
        api_client = HTBAPIClient()
        tracks_module = TracksModule(api_client)
        
        # Try to parse as integer first (track ID)
        track_id = None
        try:
            track_id = int(track_identifier)
        except ValueError:
            # If not an integer, treat as track name
            track_id = tracks_module.find_track_id_by_name(track_identifier)
            if not track_id:
                console.print(f"[red]Track not found: {track_identifier}[/red]")
                console.print("[yellow]Use 'tracks list-tracks' to see available tracks[/yellow]")
                return
        
        result = tracks_module.get_track_info(track_id)
        
        # Handle debug and json options
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Track Info API Response", json_output)
            return
        
        if result:
            info = result if isinstance(result, dict) else (result.get('data', {}) if isinstance(result, dict) else {})
            # Count modules from items
            modules_count = len(info.get('items', [])) if info.get('items') else 0
            
            console.print(Panel.fit(
                f"[bold green]Track Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}\n"
                f"Creator: {info.get('creator', {}).get('name', 'N/A') or 'N/A'}\n"
                f"Official: {info.get('official', 'N/A') or 'N/A'}\n"
                f"Modules: {modules_count}\n"
                f"Likes: {info.get('likes', 'N/A') or 'N/A'}\n"
                f"Enrolled: {info.get('enrolled', 'N/A') or 'N/A'}\n"
                f"Completed: {info.get('completed', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Track ID: {track_id}"
            ))
        else:
            console.print("[yellow]Track not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")



@tracks.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('track_identifier')
def items(track_identifier, debug, json_output):
    """List track items (machines and challenges) by ID or name"""
    try:
        api_client = HTBAPIClient()
        tracks_module = TracksModule(api_client)
        
        # Try to parse as integer first (track ID)
        track_id = None
        try:
            track_id = int(track_identifier)
        except ValueError:
            # If not an integer, treat as track name
            track_id = tracks_module.find_track_id_by_name(track_identifier)
            if not track_id:
                console.print(f"[red]Track not found: {track_identifier}[/red]")
                console.print("[yellow]Use 'tracks list-tracks' to see available tracks[/yellow]")
                return
        
        result = tracks_module.get_track_items(track_id)
        
        # Handle debug and json options
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Track Items API Response", json_output)
            return
        
        if result:
            track_info = result if isinstance(result, dict) else (result.get('data', {}) if isinstance(result, dict) else {})
            items = track_info.get('items', [])
            
            if not items:
                console.print("[yellow]No items found in this track[/yellow]")
                return
            
            # Separate machines and challenges
            machines = [item for item in items if item.get('type') == 'machine']
            challenges = [item for item in items if item.get('type') == 'challenge']
            
            # Display track info
            console.print(Panel.fit(
                f"[bold green]Track: {track_info.get('name', 'N/A')}[/bold green]\n"
                f"Difficulty: {track_info.get('difficulty', 'N/A')}\n"
                f"Total Items: {len(items)}\n"
                f"Machines: {len(machines)}\n"
                f"Challenges: {len(challenges)}",
                title=f"Track Overview (ID: {track_id})"
            ))
            
            # Display machines table
            if machines:
                console.print(f"\n[bold blue]Machines ({len(machines)})[/bold blue]")
                machine_table = Table(title="Track Machines")
                machine_table.add_column("ID", style="cyan")
                machine_table.add_column("Name", style="green")
                machine_table.add_column("Difficulty", style="yellow")
                machine_table.add_column("OS", style="magenta")
                machine_table.add_column("Status", style="blue")
                
                for machine in machines:
                    status = "✓" if machine.get('complete', False) else "○"
                    status_color = "green" if machine.get('complete', False) else "white"
                    machine_table.add_row(
                        str(machine.get('id', 'N/A')),
                        str(machine.get('name', 'N/A')),
                        str(machine.get('difficulty', 'N/A')),
                        str(machine.get('os', 'N/A')),
                        f"[{status_color}]{status}[/{status_color}]"
                    )
                
                console.print(machine_table)
            
            # Display challenges table
            if challenges:
                console.print(f"\n[bold blue]Challenges ({len(challenges)})[/bold blue]")
                challenge_table = Table(title="Track Challenges")
                challenge_table.add_column("ID", style="cyan")
                challenge_table.add_column("Name", style="green")
                challenge_table.add_column("Difficulty", style="yellow")
                challenge_table.add_column("Category", style="magenta")
                challenge_table.add_column("Status", style="blue")
                
                for challenge in challenges:
                    status = "✓" if challenge.get('complete', False) else "○"
                    status_color = "green" if challenge.get('complete', False) else "white"
                    challenge_table.add_row(
                        str(challenge.get('id', 'N/A')),
                        str(challenge.get('name', 'N/A')),
                        str(challenge.get('difficulty', 'N/A')),
                        str(challenge.get('category', 'N/A')),
                        f"[{status_color}]{status}[/{status_color}]"
                    )
                
                console.print(challenge_table)
        else:
            console.print("[yellow]Track not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@tracks.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('track_id', type=int)
def writeup(track_id, debug, json_output):
    """Get track writeup"""
    try:
        api_client = HTBAPIClient()
        tracks_module = TracksModule(api_client)
        result = tracks_module.get_track_writeup(track_id)
        
        # Handle debug and json options
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Track Writeup API Response", json_output)
            return
        
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
