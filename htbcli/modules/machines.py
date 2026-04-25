"""
Machines module for HTB CLI
"""

import click
import sys
import json
from typing import Dict, Any, Optional, Union
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.progress_bar import ProgressBar

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option
from ..config import Config
from .vpn import VPNModule

console = Console()

def format_complex_value(value: Any, indent: int = 0) -> str:
    """Format complex values (dicts, lists) in a readable way"""
    indent_str = "  " * indent
    
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = ["{"]
        for k, v in value.items():
            formatted_v = format_complex_value(v, indent + 1)
            lines.append(f"{indent_str}  {k}: {formatted_v}")
        lines.append(f"{indent_str}}}")
        return "\n".join(lines)
    elif isinstance(value, list):
        if not value:
            return "[]"
        lines = ["["]
        for i, item in enumerate(value):
            formatted_item = format_complex_value(item, indent + 1)
            lines.append(f"{indent_str}  {i}: {formatted_item}")
        lines.append(f"{indent_str}]")
        return "\n".join(lines)
    elif value is None:
        return "null"
    else:
        return str(value)

def format_response_fields(data: Dict[str, Any]) -> str:
    """Format response fields with proper handling of complex nested structures"""
    lines = []
    for key, value in data.items():
        if isinstance(value, (dict, list)) and value:
            lines.append(f"{key}:")
            lines.append(format_complex_value(value, 1))
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)

class MachinesModule:
    """Module for handling machine-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
        self.vpn_module = VPNModule(api_client)
    
    def get_machine_active(self) -> Dict[str, Any]:
        """Get active machine details"""
        return self.api.get("/machine/active")
    
    def get_machine_activity(self, machine_id: int) -> Dict[str, Any]:
        """Get machine activity"""
        return self.api.get(f"/machine/activity/{machine_id}")
    
    def get_machine_changelog(self, machine_id: int) -> Dict[str, Any]:
        """Get machine changelog"""
        return self.api.get(f"/machine/changelog/{machine_id}")
    
    def get_machine_creators(self, machine_id: int) -> Dict[str, Any]:
        """Get machine creators"""
        return self.api.get(f"/machine/creators/{machine_id}")
    
    def get_machine_graph_activity(self, machine_id: int, period: str) -> Dict[str, Any]:
        """Get machine graph activity"""
        return self.api.get(f"/machine/graph/activity/{machine_id}/{period}")
    
    def get_machine_graph_matrix(self, machine_id: int) -> Dict[str, Any]:
        """Get machine graph matrix"""
        return self.api.get(f"/machine/graph/matrix/{machine_id}")
    
    def get_machine_graph_owns_difficulty(self, machine_id: int) -> Dict[str, Any]:
        """Get machine graph difficulty"""
        return self.api.get(f"/machine/graph/owns/difficulty/{machine_id}")
    
    def get_machine_list_retired_paginated(
        self, 
        page: int = 1, 
        per_page: int = 20,
        sort_by: Optional[str] = None,
        sort_type: Optional[str] = None,
        difficulty: Optional[list] = None,
        os: Optional[list] = None,
        tags: Optional[list] = None,
        keyword: Optional[str] = None,
        show_completed: Optional[str] = None,
        free: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Get paginated list of retired machines with filtering options"""
        params = {
            "page": page,
            "per_page": per_page
        }
        
        if sort_by:
            params["sort_by"] = sort_by
        if sort_type:
            params["sort_type"] = sort_type
        if difficulty:
            params["difficulty[]"] = difficulty
        if os:
            # Pass os as a list with [] notation to indicate it's an array parameter
            # requests will format it as os[]=windows&os[]=linux or os[]=windows for single value
            params["os[]"] = os
        if tags:
            params["tags"] = tags
        if keyword:
            params["keyword"] = keyword
        if show_completed:
            params["show_completed"] = show_completed
        if free:
            params["free"] = 1
            
        return self.api.get("/machine/list/retired/paginated", params=params)
    
    def submit_machine_flag(self, flag: str, machine_id: int) -> Dict[str, Any]:
        """Submit flag for machine"""
        # Use v5 API for flag submission with both flag and machine ID
        v5_api_client = HTBAPIClient(version="v5")
        return v5_api_client.post("/machine/own", json_data={"flag": flag, "id": machine_id})
    
    def get_machine_owns_top(self, machine_id: int) -> Dict[str, Any]:
        """Get top 25 owners for a machine"""
        return self.api.get(f"/machine/owns/top/{machine_id}")
    
    def get_machine_paginated(
        self, 
        page: int = 1, 
        per_page: int = 20, 
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_type: Optional[str] = None,
        difficulty: Optional[list] = None,
        os: Optional[list] = None,
        tags: Optional[list] = None,
        keyword: Optional[str] = None,
        show_completed: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated list of machines with filtering options"""
        params = {
            "page": page,
            "per_page": per_page
        }
        if status:
            params["state"] = status
        if sort_by:
            params["sort_by"] = sort_by
        if sort_type:
            params["sort_type"] = sort_type
        if difficulty:
            params["difficulty[]"] = difficulty
        if os:
            # Pass os as a list with [] notation to indicate it's an array parameter
            # requests will format it as os[]=windows&os[]=linux or os[]=windows for single value
            params["os[]"] = os
        if tags:
            params["tags"] = tags
        if keyword:
            params["keyword"] = keyword
        if show_completed:
            params["show_completed"] = show_completed
        return self.api.get("/machine/paginated", params=params)
    
    def get_machine_profile(self, machine_slug: str) -> Dict[str, Any]:
        """Get machine profile by slug"""
        return self.api.get(f"/machine/profile/{machine_slug}")
    
    def get_machine_recommended(self) -> Dict[str, Any]:
        """Get recommended machines"""
        return self.api.get("/machine/recommended")
    
    def get_machine_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired machines"""
        return self.api.get("/machine/recommended/retired")
    
    def submit_machine_review(self, machine_id: int, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit machine review"""
        return self.api.post("/machine/review", json_data=review_data)
    
    def get_machine_reviews_user(self, machine_id: int) -> Dict[str, Any]:
        """Get user's review for machine"""
        return self.api.get(f"/machine/reviews/user/{machine_id}")
    
    def get_machine_reviews(self, machine_id: int) -> Dict[str, Any]:
        """Get machine reviews"""
        return self.api.get(f"/machine/reviews/{machine_id}")
    
    def get_machine_tags_list(self) -> Dict[str, Any]:
        """Get machine tags list"""
        return self.api.get("/machine/tags/list")
    
    def get_machine_tags(self, machine_id: int) -> Dict[str, Any]:
        """Get machine tags"""
        return self.api.get(f"/machine/tags/{machine_id}")
    
    def get_machine_todo_paginated(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get machine todo list"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/machine/todo/paginated", params=params)
    
    def get_machine_unreleased(self) -> Dict[str, Any]:
        """Get unreleased machines"""
        return self.api.get("/machine/unreleased")
    
    def get_machine_walkthrough_random(self) -> Dict[str, Any]:
        """Get random walkthrough"""
        return self.api.get("/machine/walkthrough/random")
    
    def get_machine_walkthroughs_language_list(self) -> Dict[str, Any]:
        """Get walkthrough language options"""
        return self.api.get("/machine/walkthroughs/language/list")
    
    def get_machine_walkthroughs_official_feedback_choices(self) -> Dict[str, Any]:
        """Get feedback choices"""
        return self.api.get("/machine/walkthroughs/official/feedback-choices")
    
    def get_machine_walkthroughs(self, machine_id: int) -> Dict[str, Any]:
        """Get machine walkthroughs"""
        return self.api.get(f"/machine/walkthroughs/{machine_id}")
    
    def get_machine_writeup(self, machine_id: int) -> bytes:
        """Get machine writeup (returns PDF binary data)"""
        return self.api.get_binary(f"/machine/writeup/{machine_id}")
    
    def get_machines_adventure(self, machine_id: int) -> Dict[str, Any]:
        """Get machines adventure"""
        return self.api.get(f"/machines/{machine_id}/adventure")

    def get_machines_tasks(self, machine_id: int) -> Dict[str, Any]:
        """Get machines tasks"""
        return self.api.get(f"/machines/{machine_id}/tasks")

    def submit_machine_task_flag(self, machine_id: int, task_id: int, flag: str) -> Dict[str, Any]:
        """Submit an answer to a guided-mode task question."""
        return self.api.post(f"/machines/{machine_id}/tasks/{task_id}/flag", json_data={"flag": flag})

    def resolve_machine_name_and_id(self, machine_identifier: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Resolve machine identifier to both ID and name/slug by fetching profile data.
        Returns dict with 'id', 'name', 'isGuidedEnabled', and full 'info' from profile."""
        machine_id = self.resolve_machine_id(machine_identifier)
        if machine_id is None:
            return None

        # Try to get machine profile using the identifier as slug if it's a string
        info = None
        if isinstance(machine_identifier, str) and not machine_identifier.isdigit():
            try:
                result = self.get_machine_profile(machine_identifier.lower())
                if result and 'info' in result:
                    info = result['info']
            except Exception:
                pass

        # If we couldn't get profile by slug, try active machine or search
        if info is None:
            try:
                # Try getting active machine info
                active = self.get_machine_active()
                if active and active.get('info') and active['info'].get('id') == machine_id:
                    name = active['info'].get('name', '').lower()
                    result = self.get_machine_profile(name)
                    if result and 'info' in result:
                        info = result['info']
            except Exception:
                pass

        return {
            'id': machine_id,
            'name': info.get('name', str(machine_id)) if info else str(machine_id),
            'isGuidedEnabled': info.get('isGuidedEnabled', False) if info else False,
            'info': info
        }

    def search_machine_by_name(self, machine_name: str, max_pages: int = 20) -> Optional[int]:
        """Search for a machine by name using platform search API and return its ID"""
        try:
            # Use platform search API to find machines
            from .platform import PlatformModule
            platform_module = PlatformModule(self.api)
            result = platform_module.get_search_fetch(machine_name)
            
            if not result or 'machines' not in result:
                return None
            
            machines = result['machines']
            if not machines:
                return None
            
            # Filter and rank matches
            exact_matches = []
            partial_matches = []
            
            for machine in machines:
                name = machine.get('value', '').lower()  # 'value' field contains the machine name
                machine_id = machine.get('id')
                search_term = machine_name.lower()
                
                # Check for exact match first
                if name == search_term:
                    exact_matches.append((machine_id, name))
                
                # Check for partial match (contains)
                elif search_term in name:
                    partial_matches.append((machine_id, name))
            
            # If we have exact matches, return the first one
            if exact_matches:
                return exact_matches[0][0]
            
            # If we have partial matches, return the first one
            if partial_matches:
                return partial_matches[0][0]
            
            return None
            
        except Exception as e:
            console.print(f"[red]Error searching for machine '{machine_name}': {e}[/red]")
            return None
    
    def search_machines_by_name_with_options(self, machine_name: str) -> Optional[Dict[str, Any]]:
        """Search for machines by name using platform search API and return all matches with options"""
        try:
            # Use platform search API to find machines
            from .platform import PlatformModule
            platform_module = PlatformModule(self.api)
            result = platform_module.get_search_fetch(machine_name)
            
            if not result or 'machines' not in result:
                return None
            
            machines = result['machines']
            if not machines:
                return None
            
            # Filter and rank matches
            exact_matches = []
            partial_matches = []
            
            for machine in machines:
                name = machine.get('value', '').lower()  # 'value' field contains the machine name
                machine_id = machine.get('id')
                search_term = machine_name.lower()
                
                # Check for exact match first
                if name == search_term:
                    exact_matches.append(machine)
                
                # Check for partial match (contains)
                elif search_term in name:
                    partial_matches.append(machine)
            
            # Return results with match information
            return {
                'exact_matches': exact_matches,
                'partial_matches': partial_matches,
                'total_matches': len(exact_matches) + len(partial_matches)
            }
            
        except Exception as e:
            console.print(f"[red]Error searching for machines '{machine_name}': {e}[/red]")
            return None
    
    def resolve_machine_id(self, machine_identifier: Union[int, str]) -> Optional[int]:
        """Resolve machine identifier to machine ID"""
        if isinstance(machine_identifier, int):
            return machine_identifier
        elif isinstance(machine_identifier, str):
            # Try to convert to int first (in case it's a string number)
            try:
                return int(machine_identifier)
            except ValueError:
                # Search for machine by name
                console.print(f"[blue]Searching for machine: {machine_identifier}[/blue]")
                machine_id = self.search_machine_by_name(machine_identifier)
                if machine_id:
                    console.print(f"[green]✓[/green] Found machine ID: {machine_id} for '{machine_identifier}'")
                    return machine_id
                else:
                    console.print(f"[red]Could not find machine with name: {machine_identifier}[/red]")
                    return None
        else:
            console.print(f"[red]Invalid machine identifier type: {type(machine_identifier)}[/red]")
            return None
    
    def get_active_machine_id(self) -> Optional[int]:
        """Get the ID of the currently active machine"""
        try:
            result = self.get_machine_active()
            if result and result.get('info') and result['info'].get('id'):
                machine_id = result['info']['id']
                machine_name = result['info'].get('name', 'Unknown')
                console.print(f"[blue]Using active machine: {machine_name} (ID: {machine_id})[/blue]")
                return machine_id
            else:
                console.print("[red]No active machine found[/red]")
                return None
        except Exception as e:
            console.print(f"[red]Error getting active machine: {e}[/red]")
            return None
    
    def get_vm_status(self) -> Dict[str, Any]:
        """Get VM status with complete machine information including IP and profile data"""
        # Get active machine data
        active_result = self.get_machine_active()
        
        if active_result and active_result.get('info'):
            active_info = active_result['info']
            machine_name = active_info.get('name', '').lower()
            
            # Get machine profile data for additional information
            try:
                profile_result = self.get_machine_profile(machine_name)
                if profile_result and profile_result.get('info'):
                    profile_info = profile_result['info']
                    
                    # Merge the data, prioritizing profile data for IP and other fields
                    merged_info = active_info.copy()
                    merged_info.update({
                        'ip': profile_info.get('ip', active_info.get('ip')),
                        'info_status': profile_info.get('info_status'),
                        'description': profile_info.get('description'),
                        'os': profile_info.get('os'),
                        'difficulty': profile_info.get('difficulty'),
                        'points': profile_info.get('points'),
                        'user_owns_count': profile_info.get('user_owns_count'),
                        'root_owns_count': profile_info.get('root_owns_count'),
                        'maker': profile_info.get('maker'),
                        'release_date': profile_info.get('release_date'),
                        'retired_date': profile_info.get('retired_date'),
                        'active': profile_info.get('active'),
                        'retired': profile_info.get('retired')
                    })
                    
                    return {'info': merged_info}
            except Exception:
                # If profile fetch fails, return active data as fallback
                pass
        
        return active_result
    
    def update_todo(self, product: str, product_id: int, todo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update todo list"""
        return self.api.post(f"/{product}/todo/update/{product_id}", json_data=todo_data)

# Click commands
@click.group()
def machines():
    """Machine-related commands"""
    pass

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def active(debug, json_output):
    """Get currently active machine and VM status"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_vm_status()
        
        if handle_debug_option(debug, result, "Debug: Active Machine API Response", json_output):
            return
        
        if result and result.get('info'):
            info = result['info']
            
            # Default view
            console.print(Panel.fit(
                f"[bold green]Active Machine & VM Status[/bold green]\n"
                f"Machine ID: {info.get('id', 'N/A')}\n"
                f"Name: {info.get('name', 'N/A')}\n"
                f"Type: {info.get('type', 'N/A')}\n"
                f"IP Address: {info.get('ip', 'N/A')}\n"
                f"Lab Server: {info.get('lab_server', 'N/A')}\n"
                f"VPN Server: {machines_module.vpn_module.resolve_vpn_server_name(info.get('vpn_server_id'))}\n"
                f"Expires At: {info.get('expires_at', 'N/A')}\n"
                f"Is Spawning: {info.get('isSpawning', 'N/A')}\n"
                f"Tier ID: {info.get('tier_id', 'N/A')}\n"
                f"Voted: {info.get('voted', 'N/A')}\n"
                f"Voting: {info.get('voting', 'N/A')}\n"
                f"Info Status: {info.get('info_status', 'N/A')}",
                title="Active Machine & VM Status"
            ))
        else:
            console.print("[yellow]No active machine found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")



@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def activity(machine_identifier, debug, json_output):
    """Get machine activity (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_activity(machine_id)

        if debug:
            if json_output:
                import json
                console.print(json.dumps(result, indent=2, default=str))
            else:
                console.print(result)
            return

        activity_data = None
        if result and 'info' in result:
            activity_data = result['info'].get('activity', [])
        elif result and 'data' in result:
            activity_data = result['data']

        if activity_data:
            server = result.get('info', {}).get('server', 'Unknown')
            table = Table(title=f"Machine Activity (ID: {machine_id}) - {server}")
            table.add_column("User", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Blood", style="red")
            table.add_column("Date", style="yellow")

            for entry in activity_data:
                own_type = entry.get('type', 'N/A') or 'N/A'
                blood_type = entry.get('blood_type', '') or ''

                # Color the type based on user/root
                if own_type == 'root' or blood_type == 'root':
                    type_str = f"[red]{own_type}[/red]"
                elif own_type == 'user' or blood_type == 'user':
                    type_str = f"[green]{own_type}[/green]"
                else:
                    type_str = own_type

                blood_str = f"🩸 {blood_type}" if blood_type else ""

                table.add_row(
                    str(entry.get('user_name', 'N/A') or 'N/A'),
                    type_str,
                    blood_str,
                    str(entry.get('date_diff', entry.get('date', 'N/A')) or 'N/A')
                )

            console.print(table)
        else:
            console.print("[yellow]No activity found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def changelog(machine_identifier, debug, json_output):
    """Get machine changelog (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_changelog(machine_id)
        
        if result and 'info' in result:
            changelog_data = result['info']
            
            table = Table(title=f"Machine Changelog (ID: {machine_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Type", style="yellow")
            table.add_column("Description", style="magenta")
            table.add_column("Created At", style="blue")
            table.add_column("Released", style="red")
            
            for change in changelog_data:
                table.add_row(
                    str(change.get('id', 'N/A') or 'N/A'),
                    str(change.get('title', 'N/A') or 'N/A'),
                    str(change.get('type', 'N/A') or 'N/A'),
                    str(change.get('description', 'N/A') or 'N/A'),
                    str(change.get('created_at', 'N/A') or 'N/A'),
                    str(change.get('released', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No changelog found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def creators(machine_identifier, debug, json_output):
    """Get machine creators (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_creators(machine_id)
        
        if result:
            # Handle both creator and cocreators
            creators_data = []
            if result.get('creator'):
                creators_data.extend(result['creator'])
            if result.get('cocreators'):
                creators_data.extend(result['cocreators'])
            
            if creators_data:
                table = Table(title=f"Machine Creators (ID: {machine_id})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Avatar", style="yellow")
                table.add_column("Is Respected", style="magenta")
                
                for creator in creators_data:
                    table.add_row(
                        str(creator.get('id', 'N/A') or 'N/A'),
                        str(creator.get('name', 'N/A') or 'N/A'),
                        (Config.AVATAR_BASE_URL + creator['avatar']) if creator.get('avatar') else 'N/A',
                        str(creator.get('isRespected', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No creators found[/yellow]")
        else:
            console.print("[yellow]No creators found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
@click.option('--status', default='active', type=click.Choice(['active', 'retired', 'all']), help='Machine status (active/retired/all). Use "all" to search both active and retired machines.')
@click.option('--sort-by', 
              type=click.Choice(['release-date', 'name', 'user-owns', 'system-owns', 'rating', 'user-difficulty']),
              help='Sort by field')
@click.option('--sort-type', 
              type=click.Choice(['asc', 'desc']),
              help='Sort type (asc or desc)')
@click.option('--difficulty', 
              multiple=True,
              type=click.Choice(['very-easy', 'easy', 'medium', 'hard', 'insane']),
              help='Filter by difficulty (can be used multiple times)')
@click.option('--os', 
              multiple=True,
              type=click.Choice(['linux', 'windows', 'freebsd', 'openbsd', 'other']),
              help='Filter by OS (can be used multiple times)')
@click.option('--tags', 
              multiple=True,
              type=int,
              help='Filter by tag ID (can be used multiple times)')
@click.option('--keyword', 
              help='Search keyword')
@click.option('--show-completed', 
              type=click.Choice(['complete', 'incomplete']),
              help='Show completed or incomplete machines')
@click.option('--free', 
              is_flag=True,
              help='Show only free machines (retired machines only)')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def list_machines(page, per_page, status, sort_by, sort_type, difficulty, os, tags, keyword, show_completed, free, responses, option, debug, json_output):
    """List machines with filtering options"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Convert difficulty and os from tuples to lists if they exist
        difficulty_list = list(difficulty) if difficulty else None
        os_list = list(os) if os else None
        tags_list = list(tags) if tags else None
        
        # Handle 'all' status by searching both active and retired
        if status == 'all':
            console.print("[blue]Searching both active and retired machines...[/blue]")
            
            # Get active machines
            active_result = machines_module.get_machine_paginated(
                page=page, 
                per_page=per_page, 
                status='active',
                sort_by=sort_by,
                sort_type=sort_type,
                difficulty=difficulty_list,
                os=os_list,
                tags=tags_list,
                keyword=keyword,
                show_completed=show_completed
            )
            
            # Get retired machines
            retired_result = machines_module.get_machine_list_retired_paginated(
                page=page, 
                per_page=per_page,
                sort_by=sort_by,
                sort_type=sort_type,
                difficulty=difficulty_list,
                os=os_list,
                tags=tags_list,
                keyword=keyword,
                show_completed=show_completed,
                free=free
            )
            
            # Combine results
            combined_data = []
            if active_result and 'data' in active_result:
                active_data = active_result['data']['data'] if isinstance(active_result['data'], dict) and 'data' in active_result['data'] else active_result['data']
                if active_data:
                    combined_data.extend(active_data)
            
            if retired_result and 'data' in retired_result:
                retired_data = retired_result['data']['data'] if isinstance(retired_result['data'], dict) and 'data' in retired_result['data'] else retired_result['data']
                if retired_data:
                    combined_data.extend(retired_data)
            
            # Create combined result structure
            result = {
                'data': combined_data,
                'meta': {
                    'current_page': page,
                    'per_page': per_page,
                    'total': len(combined_data)
                }
            }
        elif status == 'retired':
            result = machines_module.get_machine_list_retired_paginated(
                page=page, 
                per_page=per_page,
                sort_by=sort_by,
                sort_type=sort_type,
                difficulty=difficulty_list,
                os=os_list,
                tags=tags_list,
                keyword=keyword,
                show_completed=show_completed,
                free=free
            )
        else:
            result = machines_module.get_machine_paginated(
                page=page, 
                per_page=per_page, 
                status=status,
                sort_by=sort_by,
                sort_type=sort_type,
                difficulty=difficulty_list,
                os=os_list,
                tags=tags_list,
                keyword=keyword,
                show_completed=show_completed
            )
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Machines List", json_output)
            return
        
        if result and 'data' in result:
            machines_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            if responses:
                # Show all available fields for first machine
                if machines_data:
                    first_machine = machines_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Machines[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_machine.items()])}",
                        title=f"Machines - All Fields (First Item, Page {page})"
                    ))
            elif option:
                # Show default table with additional specified fields
                table = Table(title=f"Machines (Page {page})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("OS", style="yellow")
                table.add_column("Difficulty", style="magenta")
                table.add_column("Rating", style="blue")
                table.add_column("Status", style="red")
                
                # Add additional columns for specified fields
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for machine in machines_data:
                    # Default row data
                    row = [
                        str(machine.get('id', 'N/A') or 'N/A'),
                        str(machine.get('name', 'N/A') or 'N/A'),
                        str(machine.get('os', 'N/A') or 'N/A'),
                        str(machine.get('difficultyText', 'N/A') or 'N/A'),
                        str(machine.get('star', 'N/A') or 'N/A'),
                        'Active' if status == 'active' else 'Retired' if status == 'retired' else 'N/A'
                    ]
                    
                    # Add additional specified fields
                    for field in option:
                        row.append(str(machine.get(field, 'N/A') or 'N/A'))
                    
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Show default table
                table = Table(title=f"Machines (Page {page})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("OS", style="yellow")
                table.add_column("Difficulty", style="magenta")
                table.add_column("Rating", style="blue")
                table.add_column("Status", style="red")
                
                try:
                    for machine in machines_data:
                        table.add_row(
                            str(machine.get('id', 'N/A') or 'N/A'),
                            str(machine.get('name', 'N/A') or 'N/A'),
                            str(machine.get('os', 'N/A') or 'N/A'),
                            str(machine.get('difficultyText', 'N/A') or 'N/A'),
                            str(machine.get('star', 'N/A') or 'N/A'),
                            'Active' if status == 'active' else 'Retired' if status == 'retired' else 'N/A'
                        )
                    
                    console.print(table)
                except Exception as e:
                    console.print(f"[yellow]Error processing machines data: {e}[/yellow]")
        else:
            # Provide helpful message when no machines found
            filters_applied = []
            if show_completed:
                filters_applied.append(f"show_completed={show_completed}")
            if difficulty_list:
                filters_applied.append(f"difficulty={', '.join(difficulty_list)}")
            if os_list:
                filters_applied.append(f"os={', '.join(os_list)}")
            if status:
                filters_applied.append(f"status={status}")
            
            message = "[yellow]No machines found[/yellow]"
            if filters_applied:
                message += f" with filters: {', '.join(filters_applied)}"
            
            # Suggest checking retired machines if searching active
            if status == 'active' or status is None:
                message += "\n[yellow]Tip: Try adding [bold]--status retired[/bold] to search retired machines as well[/yellow]"
            
            console.print(message)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.argument('machine_slug')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def profile(machine_slug, responses, option):
    """Get machine profile by slug"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_profile(machine_slug)
        
        if result and 'info' in result:
            info = result['info']
            
            if responses:
                # Show all available fields with proper formatting for complex structures
                formatted_fields = format_response_fields(info)
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for Machine Profile[/bold green]\n"
                    f"{formatted_fields}",
                    title=f"Machine: {machine_slug} - All Fields"
                ))
            elif option:
                # Show only specified fields
                selected_info = {}
                for field in option:
                    if field in info:
                        value = info[field]
                        if field == 'avatar' and value:
                            value = Config.AVATAR_BASE_URL + value
                        selected_info[field] = value
                    else:
                        console.print(f"[yellow]Field '{field}' not found in response[/yellow]")
                
                if selected_info:
                    formatted_fields = format_response_fields(selected_info)
                    console.print(Panel.fit(
                        f"[bold green]Selected Fields[/bold green]\n"
                        f"{formatted_fields}",
                        title=f"Machine: {machine_slug} - Selected Fields"
                    ))
            else:
                # Default view with enhanced information
                maker_name = info.get('maker', {}).get('name', 'N/A') if info.get('maker') else 'N/A'
                difficulty_text = info.get('difficultyText', 'N/A')
                stars = info.get('stars', 'N/A')
                auth_user_owns = 'Yes' if info.get('authUserInUserOwns') else 'No'
                auth_root_owns = 'Yes' if info.get('authUserInRootOwns') else 'No'
                info_status = info.get('info_status', 'N/A')
                
                console.print(Panel.fit(
                    f"[bold green]Machine Profile[/bold green]\n"
                    f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                    f"OS: {info.get('os', 'N/A') or 'N/A'}\n"
                    f"Difficulty: {difficulty_text}\n"
                    f"Stars: {stars}\n"
                    f"Status: {'Active' if info.get('active') else 'Retired' if info.get('retired') else 'N/A'}\n"
                    f"User Owns: {info.get('user_owns_count', 'N/A') or 'N/A'}\n"
                    f"Root Owns: {info.get('root_owns_count', 'N/A') or 'N/A'}\n"
                    f"Maker: {maker_name}\n"
                    f"You Own User: {auth_user_owns}\n"
                    f"You Own Root: {auth_root_owns}\n"
                    f"Release Date: {info.get('release', 'N/A') or 'N/A'}\n"
                    f"IP: {info.get('ip', 'N/A') or 'N/A'}\n"
                    f"Info Status: {info_status}",
                    title=f"Machine: {machine_slug}"
                ))
        else:
            console.print("[yellow]Machine not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier', required=False)
@click.argument('flag', required=False)
def submit(machine_identifier, flag, debug, json_output):
    """Submit flag for machine. Uses active machine if no machine specified. Flag can be provided as argument or piped from stdin."""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Handle argument parsing - if only one argument is provided, it's the flag
        if machine_identifier is not None and flag is None:
            # Only one argument provided - treat it as the flag
            flag = machine_identifier
            machine_identifier = None
        
        # Determine machine ID
        machine_id = None
        if machine_identifier is None:
            # Use active machine
            machine_id = machines_module.get_active_machine_id()
            if machine_id is None:
                console.print("[red]No machine specified and no active machine found[/red]")
                return
        else:
            # Resolve machine identifier to machine ID
            machine_id = machines_module.resolve_machine_id(machine_identifier)
            if machine_id is None:
                console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
                return
        
        # Get flag from argument or stdin
        if flag is None:
            # Read from stdin
            if not sys.stdin.isatty():
                flag = sys.stdin.read().strip()
                if not flag:
                    console.print("[red]No flag provided via stdin[/red]")
                    return
            else:
                console.print("[red]No flag provided. Use: htbcli machines submit [machine] <flag> or pipe flag via stdin[/red]")
                return
        
        result = machines_module.submit_machine_flag(flag, machine_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Flag Submission Result[/bold green]\n"
                f"Machine ID: {machine_id}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Flag Submission"
            ))
        else:
            console.print("[yellow]No result from flag submission[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def recommended(debug, json_output):
    """Get recommended machines"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_recommended()
        
        if handle_debug_option(debug, result, "Debug: Recommended Machines API Response", json_output):
            return
        
        if result:
            # Handle card1 and card2 structure
            recommended_data = []
            if result.get('card1'):
                recommended_data.append(result['card1'])
            if result.get('card2'):
                recommended_data.append(result['card2'])
            
            if recommended_data:
                table = Table(title="Recommended Machines")
                table.add_column("Name", style="cyan")
                table.add_column("OS", style="green")
                table.add_column("Difficulty", style="yellow")
                table.add_column("Points", style="magenta")
                
                for machine in recommended_data:
                    table.add_row(
                        str(machine.get('name', 'N/A') or 'N/A'),
                        str(machine.get('os', 'N/A') or 'N/A'),
                        str(machine.get('difficulty', 'N/A') or 'N/A'),
                        str(machine.get('points', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No recommended machines found[/yellow]")
        else:
            console.print("[yellow]No recommended machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def tags(debug, json_output):
    """Get machine tags list"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_tags_list()
        
        if result and 'info' in result:
            tags_data = result['info']
            
            table = Table(title="Machine Tags")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Category", style="yellow")
            
            for tag in tags_data:
                table.add_row(
                    str(tag.get('id', 'N/A') or 'N/A'),
                    str(tag.get('name', 'N/A') or 'N/A'),
                    str(tag.get('category', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No tags found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def unreleased(debug, json_output):
    """Get unreleased machines"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_unreleased()
        
        if debug:
            from htbcli.debug_handler import debug_response
            debug_response(result, "Debug: Unreleased Machines API Response", json_output)
            return
        
        if result and 'data' in result:
            unreleased_data = result['data']
            
            table = Table(title="Unreleased Machines")
            table.add_column("Name", style="cyan")
            table.add_column("OS", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Release Date", style="magenta")
            table.add_column("Creators", style="blue")
            table.add_column("Retiring Machine", style="red")
            table.add_column("Retiring Difficulty", style="yellow")
            
            for machine in unreleased_data:
                # Use correct field names from API specification
                difficulty = machine.get('difficulty_text', 'N/A') or 'N/A'
                release_date = machine.get('release', 'N/A') or 'N/A'
                
                # Handle creators information
                creators = []
                first_creator = machine.get('firstCreator')
                if first_creator and isinstance(first_creator, list) and len(first_creator) > 0:
                    creators.append(first_creator[0].get('name', 'Unknown'))
                elif first_creator and isinstance(first_creator, dict):
                    creators.append(first_creator.get('name', 'Unknown'))
                
                co_creators = machine.get('coCreators')
                if co_creators and isinstance(co_creators, list):
                    for co_creator in co_creators:
                        if isinstance(co_creator, dict):
                            creators.append(co_creator.get('name', 'Unknown'))
                
                creators_str = ', '.join(creators) if creators else 'N/A'
                
                # Handle retiring machine information
                retiring_machine = 'N/A'
                retiring_difficulty = 'N/A'
                retiring_info = machine.get('retiring')
                if retiring_info and isinstance(retiring_info, dict):
                    retiring_machine = retiring_info.get('name', 'N/A') or 'N/A'
                    retiring_difficulty = retiring_info.get('difficulty_text', 'N/A') or 'N/A'
                
                table.add_row(
                    str(machine.get('name', 'N/A') or 'N/A'),
                    str(machine.get('os', 'N/A') or 'N/A'),
                    str(difficulty),
                    str(release_date),
                    creators_str,
                    str(retiring_machine),
                    str(retiring_difficulty)
                )
            
            console.print(table)
        else:
            console.print("[yellow]No unreleased machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.argument('machine_identifier')
@click.option('--period', default='1m', help='Time period for graph')
def graph_activity(machine_identifier, period):
    """Get machine graph activity (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_graph_activity(machine_id, period)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Machine Graph Activity[/bold green]\n"
                f"Machine ID: {machine_id}\n"
                f"Period: {period}\n"
                f"Data: {result}",
                title="Machine Graph Activity"
            ))
        else:
            console.print("[yellow]No graph activity data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def graph_matrix(machine_identifier, debug, json_output):
    """Get machine graph matrix (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_graph_matrix(machine_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Machine Graph Matrix[/bold green]\n"
                f"Machine ID: {machine_id}\n"
                f"Data: {result}",
                title="Machine Graph Matrix"
            ))
        else:
            console.print("[yellow]No graph matrix data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def graph_difficulty(machine_identifier, debug, json_output):
    """Get machine graph difficulty (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_graph_owns_difficulty(machine_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Machine Graph Difficulty[/bold green]\n"
                f"Machine ID: {machine_id}\n"
                f"Data: {result}",
                title="Machine Graph Difficulty"
            ))
        else:
            console.print("[yellow]No graph difficulty data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
@click.option('--sort-by', 
              type=click.Choice(['release-date', 'name', 'user-owns', 'system-owns', 'rating', 'user-difficulty']),
              help='Sort by field')
@click.option('--sort-type', 
              type=click.Choice(['asc', 'desc']),
              help='Sort type (asc or desc)')
@click.option('--difficulty', 
              multiple=True,
              type=click.Choice(['very-easy', 'easy', 'medium', 'hard', 'insane']),
              help='Filter by difficulty (can be used multiple times)')
@click.option('--os', 
              multiple=True,
              type=click.Choice(['linux', 'windows', 'freebsd', 'openbsd', 'other']),
              help='Filter by OS (can be used multiple times)')
@click.option('--tags', 
              multiple=True,
              type=int,
              help='Filter by tag ID (can be used multiple times)')
@click.option('--keyword', 
              help='Search keyword')
@click.option('--show-completed', 
              type=click.Choice(['complete', 'incomplete']),
              help='Show completed or incomplete machines')
@click.option('--free', 
              is_flag=True,
              help='Show only free machines')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def retired_list(page, per_page, sort_by, sort_type, difficulty, os, tags, keyword, show_completed, free, debug, json_output):
    """Get paginated list of retired machines with filtering options"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Convert difficulty and os from tuples to lists if they exist
        difficulty_list = list(difficulty) if difficulty else None
        os_list = list(os) if os else None
        tags_list = list(tags) if tags else None
        
        result = machines_module.get_machine_list_retired_paginated(
            page=page, 
            per_page=per_page,
            sort_by=sort_by,
            sort_type=sort_type,
            difficulty=difficulty_list,
            os=os_list,
            tags=tags_list,
            keyword=keyword,
            show_completed=show_completed,
            free=free
        )
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Retired Machines", json_output)
            return
        
        if result and 'data' in result:
            machines_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Retired Machines (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("OS", style="yellow")
            table.add_column("Difficulty", style="magenta")
            table.add_column("Rating", style="blue")
            
            for machine in machines_data:
                table.add_row(
                    str(machine.get('id', 'N/A') or 'N/A'),
                    str(machine.get('name', 'N/A') or 'N/A'),
                    str(machine.get('os', 'N/A') or 'N/A'),
                    str(machine.get('difficultyText', 'N/A') or 'N/A'),
                    str(machine.get('star', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No retired machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def owns_top(machine_identifier, debug, json_output):
    """Get top 25 owners for a machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_owns_top(machine_id)
        
        if result and 'info' in result:
            owners_data = result['info']

            table = Table(title=f"Top Owners for Machine (ID: {machine_id})", show_lines=False)
            table.add_column("#", style="cyan", no_wrap=True)
            table.add_column("Name", style="green", no_wrap=True)
            table.add_column("Rank", style="yellow", no_wrap=True)
            table.add_column("User Own", style="magenta", no_wrap=True)
            table.add_column("Root Own", style="blue", no_wrap=True)
            table.add_column("Notes", style="red", no_wrap=True)

            for owner in owners_data:
                notes = []
                if owner.get('is_user_blood'):
                    notes.append("🩸 USR")
                if owner.get('is_root_blood'):
                    notes.append("🩸 ROOT")

                root_date = owner.get('own_date', '')
                user_date = owner.get('user_own_date', '')
                if root_date and user_date and root_date < user_date:
                    notes.append("⚠ ROOT<USER")
                elif root_date and user_date and root_date == user_date:
                    notes.append("⚠ SAME")

                # Show time only (HH:MM:SS) with the own_time in parentheses
                def fmt_own(date_str, time_str):
                    if not date_str:
                        return 'N/A'
                    time_part = date_str.split('T')[1].replace('.000000Z', '') if 'T' in date_str else date_str
                    return f"{time_part} ({time_str})" if time_str else time_part

                user_time = owner.get('user_own_time', '') or ''
                root_time = owner.get('root_own_time', '') or ''

                table.add_row(
                    str(owner.get('position', 'N/A') or 'N/A'),
                    str(owner.get('name', 'N/A') or 'N/A'),
                    str(owner.get('rank_text', 'N/A') or 'N/A'),
                    fmt_own(user_date, user_time),
                    fmt_own(root_date, root_time),
                    " ".join(notes) if notes else ""
                )

            console.print(table)
        else:
            console.print("[yellow]No owners data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command(name='owns-timeline')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
@click.argument('machine_identifier')
def owns_timeline(machine_identifier, debug, json_output):
    """Show machine owners ranked by who completed both user+root first"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)

        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return

        result = machines_module.get_machine_owns_top(machine_id)

        if debug:
            if json_output:
                import json
                console.print(json.dumps(result, indent=2, default=str))
            else:
                console.print(result)
            return

        if not result or 'info' not in result:
            console.print("[yellow]No owners data found[/yellow]")
            return

        owners_data = result['info']

        # Build list with completion time = max(user_own_date, root_own_date)
        completed = []
        for owner in owners_data:
            root_date = owner.get('own_date', '')
            user_date = owner.get('user_own_date', '')
            if not root_date or not user_date:
                continue
            completion_time = max(root_date, user_date)
            completed.append({
                **owner,
                'completion_time': completion_time,
                'root_first': root_date < user_date,
                'same_time': root_date == user_date,
            })

        # Sort by completion time (first to finish both flags = #1)
        completed.sort(key=lambda x: x['completion_time'])

        table = Table(title=f"Owns Timeline for Machine (ID: {machine_id})")
        table.add_column("#", style="cyan", no_wrap=True)
        table.add_column("Name", style="green", no_wrap=True)
        table.add_column("Rank", style="yellow", no_wrap=True)
        table.add_column("User Own", style="magenta", no_wrap=True)
        table.add_column("Root Own", style="blue", no_wrap=True)
        table.add_column("Completed", style="white bold", no_wrap=True)
        table.add_column("Notes", style="red", no_wrap=True)

        def fmt_time(date_str):
            if not date_str or 'T' not in date_str:
                return 'N/A'
            return date_str.split('T')[1].replace('.000000Z', '')

        for i, owner in enumerate(completed, 1):
            notes = []
            if owner.get('is_user_blood'):
                notes.append("🩸 USR")
            if owner.get('is_root_blood'):
                notes.append("🩸 ROOT")
            if owner['root_first']:
                notes.append("⚠ ROOT<USER")
            elif owner['same_time']:
                notes.append("⚠ SAME")

            table.add_row(
                str(i),
                str(owner.get('name', 'N/A') or 'N/A'),
                str(owner.get('rank_text', 'N/A') or 'N/A'),
                fmt_time(owner.get('user_own_date', '')),
                fmt_time(owner.get('own_date', '')),
                fmt_time(owner['completion_time']),
                " ".join(notes) if notes else ""
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def recommended_retired(debug, json_output):
    """Get recommended retired machines"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_recommended_retired()
        
        if result:
            # The response has card1 and card2 directly
            recommended_data = [result.get('card1'), result.get('card2')] if result.get('card1') and result.get('card2') else []
            
            table = Table(title="Recommended Retired Machines")
            table.add_column("Name", style="cyan")
            table.add_column("OS", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Release Date", style="magenta")
            
            for machine in recommended_data:
                if machine:
                    table.add_row(
                        str(machine.get('name', 'N/A') or 'N/A'),
                        str(machine.get('os', 'N/A') or 'N/A'),
                        str(machine.get('difficultyText', 'N/A') or 'N/A'),
                        str(machine.get('release', 'N/A') or 'N/A')
                    )
            
            console.print(table)
        else:
            console.print("[yellow]No recommended retired machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def reviews(machine_identifier, debug, json_output):
    """Get machine reviews (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_reviews(machine_id)
        
        if result and 'data' in result:
            reviews_data = result['data']
            
            table = Table(title=f"Machine Reviews (ID: {machine_id})")
            table.add_column("User", style="cyan")
            table.add_column("Rating", style="green")
            table.add_column("Comment", style="yellow")
            table.add_column("Date", style="magenta")
            
            for review in reviews_data:
                table.add_row(
                    str(review.get('user', 'N/A') or 'N/A'),
                    str(review.get('rating', 'N/A') or 'N/A'),
                    str(review.get('comment', 'N/A') or 'N/A'),
                    str(review.get('date', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No reviews found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def reviews_user(machine_identifier, debug, json_output):
    """Get user's review for machine (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_reviews_user(machine_id)
        
        if result and 'data' in result:
            review_data = result['data']
            
            console.print(Panel.fit(
                f"[bold green]User Review for Machine[/bold green]\n"
                f"Machine ID: {machine_id}\n"
                f"Rating: {review_data.get('rating', 'N/A') or 'N/A'}\n"
                f"Comment: {review_data.get('comment', 'N/A') or 'N/A'}\n"
                f"Date: {review_data.get('date', 'N/A') or 'N/A'}",
                title="User Review"
            ))
        else:
            console.print("[yellow]No user review found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def machine_tags(machine_identifier, debug, json_output):
    """Get machine tags (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_tags(machine_id)
        
        if result and 'data' in result:
            tags_data = result['data']
            
            table = Table(title=f"Machine Tags (ID: {machine_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Type", style="yellow")
            
            for tag in tags_data:
                table.add_row(
                    str(tag.get('id', 'N/A') or 'N/A'),
                    str(tag.get('name', 'N/A') or 'N/A'),
                    str(tag.get('type', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No machine tags found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
def todo_list(page, per_page):
    """Get machine todo list"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_todo_paginated(page, per_page)
        
        if result and 'data' in result:
            todo_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Machine Todo List (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("OS", style="yellow")
            table.add_column("Difficulty", style="magenta")
            table.add_column("Rating", style="blue")
            
            for machine in todo_data:
                table.add_row(
                    str(machine.get('id', 'N/A') or 'N/A'),
                    str(machine.get('name', 'N/A') or 'N/A'),
                    str(machine.get('os', 'N/A') or 'N/A'),
                    str(machine.get('difficultyText', 'N/A') or 'N/A'),
                    str(machine.get('star', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No todo machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def walkthrough_random(debug, json_output):
    """Get random walkthrough"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_walkthrough_random()
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Random Walkthrough[/bold green]\n"
                f"Data: {result}",
                title="Random Walkthrough"
            ))
        else:
            console.print("[yellow]No random walkthrough found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def walkthrough_languages(debug, json_output):
    """Get walkthrough language options"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_walkthroughs_language_list()
        
        if result and 'data' in result:
            languages_data = result['data']
            
            table = Table(title="Walkthrough Languages")
            table.add_column("Code", style="cyan")
            table.add_column("Name", style="green")
            
            for language in languages_data:
                table.add_row(
                    str(language.get('code', 'N/A') or 'N/A'),
                    str(language.get('name', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No languages found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

def walkthrough_feedback_choices(debug, json_output):
    """Get walkthrough feedback choices"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_walkthroughs_official_feedback_choices()
        
        if result and 'data' in result:
            choices_data = result['data']
            
            table = Table(title="Walkthrough Feedback Choices")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            
            for choice in choices_data:
                table.add_row(
                    str(choice.get('id', 'N/A') or 'N/A'),
                    str(choice.get('name', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No feedback choices found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def walkthroughs(machine_identifier, debug, json_output):
    """Get machine walkthroughs (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_walkthroughs(machine_id)
        
        if result and 'data' in result:
            walkthroughs_data = result['data']
            
            table = Table(title=f"Machine Walkthroughs (ID: {machine_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Language", style="yellow")
            table.add_column("Author", style="magenta")
            
            for walkthrough in walkthroughs_data:
                table.add_row(
                    str(walkthrough.get('id', 'N/A') or 'N/A'),
                    str(walkthrough.get('title', 'N/A') or 'N/A'),
                    str(walkthrough.get('language', 'N/A') or 'N/A'),
                    str(walkthrough.get('author', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No walkthroughs found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
@click.option('--output', '-o', help='Output file path (default: machine_name_writeup.pdf)')

@click.argument('machine_identifier')
def writeup(machine_identifier, debug, json_output, output):
    """Get machine writeup (accepts machine ID or name) - downloads PDF file"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        # Get machine name for filename if not provided
        machine_name = machine_identifier
        if machine_id:
            try:
                machine_info = machines_module.get_machine_info(machine_id)
                if machine_info and 'data' in machine_info and 'name' in machine_info['data']:
                    machine_name = machine_info['data']['name']
            except:
                pass  # Use original identifier if we can't get the name
        
        # Determine output filename
        if output:
            output_path = output
        else:
            # Create safe filename from machine name
            safe_name = "".join(c for c in machine_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            output_path = f"{safe_name}_writeup.pdf"
        
        console.print(f"[blue]Downloading writeup for machine: {machine_name} (ID: {machine_id})[/blue]")
        
        # Get the PDF binary data
        pdf_data = machines_module.get_machine_writeup(machine_id)
        
        if pdf_data:
            # Save the PDF file
            with open(output_path, 'wb') as f:
                f.write(pdf_data)
            
            console.print(f"[green]✓[/green] Writeup downloaded successfully: {output_path}")
            console.print(f"[blue]File size: {len(pdf_data)} bytes[/blue]")
        else:
            console.print("[yellow]No writeup found for this machine[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
@click.option('--show-hints', is_flag=True, help='Show hints for pending steps')
@click.argument('machine_identifier')
def adventure(machine_identifier, debug, json_output, show_hints):
    """Get machine adventure steps (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)

        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return

        result = machines_module.get_machines_adventure(machine_id)

        if handle_debug_option(debug, result, f"Debug: Machine Adventure API Response (ID: {machine_id})", json_output):
            return

        if result and 'data' in result:
            steps = result['data']

            if not steps:
                console.print("[yellow]No adventure steps found for this machine.[/yellow]")
                return

            completed_count = sum(1 for s in steps if s.get('completed'))
            total_count = len(steps)

            table = Table(title=f"Machine Adventure (ID: {machine_id}) — {completed_count}/{total_count} completed")
            table.add_column("#", style="dim")
            table.add_column("Title", style="green")
            table.add_column("Description", style="yellow", max_width=45)
            table.add_column("Type", style="magenta")
            table.add_column("Flag Format", style="dim")
            table.add_column("Hint", style="cyan", max_width=30)
            table.add_column("Status", style="bold")

            for idx, step in enumerate(steps, 1):
                completed = step.get('completed', False)
                status = "[green]✓ Done[/green]" if completed else "[red]✗ Pending[/red]"

                task_type = step.get('type', {})
                if isinstance(task_type, dict):
                    type_text = task_type.get('text', 'N/A')
                else:
                    type_text = str(task_type) if task_type else 'N/A'

                hint = step.get('hint', '') or ''
                if hint and not show_hints and not completed:
                    hint = "[dim]--show-hints[/dim]"

                table.add_row(
                    str(idx),
                    str(step.get('title', 'N/A') or 'N/A'),
                    str(step.get('description', '') or ''),
                    str(type_text),
                    str(step.get('masked_flag', '') or ''),
                    hint if completed or show_hints else "[dim]--show-hints[/dim]" if step.get('hint') else '',
                    status
                )

            console.print(table)
        else:
            console.print("[yellow]No adventure data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.argument('machine_name')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def search(machine_name, debug, json_output):
    """Search for machines by name and show all matches"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        search_results = machines_module.search_machines_by_name_with_options(machine_name)
        
        if debug or json_output:
            handle_debug_option(debug, search_results, "Debug: Machine Search Results", json_output)
            return
        
        if not search_results or search_results['total_matches'] == 0:
            console.print(f"[yellow]No machines found with name: {machine_name}[/yellow]")
            return
        
        # Display exact matches first
        if search_results['exact_matches']:
            table = Table(title=f"Exact Matches for '{machine_name}'")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Avatar", style="yellow")
            table.add_column("Tier", style="magenta")
            table.add_column("Starting Point", style="blue")
            
            for machine in search_results['exact_matches']:
                avatar_status = "Yes" if machine.get('avatar') else "No"
                tier_status = str(machine.get('tierId', 'N/A') or 'N/A')
                sp_status = "Yes" if machine.get('isSp') else "No"
                table.add_row(
                    str(machine.get('id', 'N/A') or 'N/A'),
                    str(machine.get('value', 'N/A') or 'N/A'),
                    avatar_status,
                    tier_status,
                    sp_status
                )
            console.print(table)
        
        # Display partial matches
        if search_results['partial_matches']:
            table = Table(title=f"Partial Matches for '{machine_name}'")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Avatar", style="yellow")
            table.add_column("Tier", style="magenta")
            table.add_column("Starting Point", style="blue")
            
            for machine in search_results['partial_matches']:
                avatar_status = "Yes" if machine.get('avatar') else "No"
                tier_status = str(machine.get('tierId', 'N/A') or 'N/A')
                sp_status = "Yes" if machine.get('isSp') else "No"
                table.add_row(
                    str(machine.get('id', 'N/A') or 'N/A'),
                    str(machine.get('value', 'N/A') or 'N/A'),
                    avatar_status,
                    tier_status,
                    sp_status
                )
            console.print(table)
        
        # Show summary
        total = search_results['total_matches']
        exact = len(search_results['exact_matches'])
        partial = len(search_results['partial_matches'])
        
        console.print(Panel.fit(
            f"[bold green]Search Summary[/bold green]\n"
            f"Total matches: {total}\n"
            f"Exact matches: {exact}\n"
            f"Partial matches: {partial}",
            title="Machine Search Results"
        ))
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('machine_identifier')
def tasks(machine_identifier, debug, json_output):
    """Get machine tasks (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)

        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return

        result = machines_module.get_machines_tasks(machine_id)

        if handle_debug_option(debug, result, f"Debug: Machine Tasks API Response (ID: {machine_id})", json_output):
            return

        if result and 'data' in result:
            tasks_data = result['data']

            if not tasks_data:
                console.print("[yellow]No tasks found for this machine. Guided mode may not be enabled.[/yellow]")
                return

            completed_count = sum(1 for t in tasks_data if t.get('completed'))
            total_count = len(tasks_data)

            table = Table(title=f"Machine Tasks (ID: {machine_id}) — {completed_count}/{total_count} completed")
            table.add_column("#", style="dim")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Description", style="yellow", max_width=50)
            table.add_column("Type", style="magenta")
            table.add_column("Flag Format", style="dim")
            table.add_column("Status", style="bold")

            for idx, task in enumerate(tasks_data, 1):
                task_type = task.get('type', {})
                if isinstance(task_type, dict):
                    type_text = task_type.get('text', 'N/A')
                else:
                    type_text = str(task_type) if task_type else 'N/A'

                completed = task.get('completed', False)
                status = "[green]✓ Done[/green]" if completed else "[red]✗ Pending[/red]"

                table.add_row(
                    str(idx),
                    str(task.get('id', 'N/A') or 'N/A'),
                    str(task.get('title', 'N/A') or 'N/A'),
                    str(task.get('description', '') or ''),
                    str(type_text),
                    str(task.get('masked_flag', '') or ''),
                    status
                )

            console.print(table)
        else:
            console.print("[yellow]No tasks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
@click.option('--show-hints', is_flag=True, help='Show hints for pending tasks')
@click.argument('machine_identifier')
def guided(machine_identifier, debug, json_output, show_hints):
    """Interactive guided mode for retired machines. Shows step-by-step tasks to solve the machine."""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)

        # Resolve machine identifier to ID and get profile info
        machine_data = machines_module.resolve_machine_name_and_id(machine_identifier)
        if machine_data is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return

        machine_id = machine_data['id']
        machine_name = machine_data['name']
        is_guided = machine_data.get('isGuidedEnabled', False)

        if not is_guided:
            console.print(f"[yellow]Guided mode is not enabled for machine '{machine_name}' (ID: {machine_id}).[/yellow]")
            console.print("[dim]Guided mode is typically available for retired machines. Trying to fetch tasks anyway...[/dim]")

        # Fetch both tasks and adventure data
        tasks_result = machines_module.get_machines_tasks(machine_id)
        adventure_result = machines_module.get_machines_adventure(machine_id)

        if debug or json_output:
            combined = {"tasks": tasks_result, "adventure": adventure_result}
            handle_debug_option(debug, combined, f"Debug: Guided Mode Data (ID: {machine_id})", json_output)
            return

        # Prefer tasks data (has richer structure with hints, prerequisites), fall back to adventure
        tasks_data = tasks_result.get('data', []) if tasks_result else []
        adventure_data = adventure_result.get('data', []) if adventure_result else []

        # Use tasks data if available (richer), otherwise adventure
        steps = tasks_data if tasks_data else adventure_data

        if not steps:
            console.print(f"[yellow]No guided steps found for machine '{machine_name}' (ID: {machine_id}).[/yellow]")
            console.print("[dim]This machine may not support guided mode.[/dim]")
            return

        completed_count = sum(1 for s in steps if s.get('completed'))
        total_count = len(steps)
        task_steps = [s for s in steps if s.get('type', {}).get('text') == 'task']
        flag_steps = [s for s in steps if s.get('type', {}).get('text') in ('user', 'root')]

        # --- Header ---
        if total_count > 0:
            progress_pct = (completed_count / total_count) * 100

            if completed_count == total_count:
                bar_style = "green"
                status_label = "[bold green]COMPLETED[/bold green]"
            elif completed_count > 0:
                bar_style = "yellow"
                status_label = "[bold yellow]IN PROGRESS[/bold yellow]"
            else:
                bar_style = "red"
                status_label = "[bold red]NOT STARTED[/bold red]"

            # Machine info line
            info = machine_data.get('info') or {}
            os_name = info.get('os', '')
            difficulty = info.get('difficultyText', '')
            info_parts = [f"[bold white]{machine_name}[/bold white]"]
            if os_name:
                info_parts.append(f"[dim]{os_name}[/dim]")
            if difficulty:
                info_parts.append(f"[dim]{difficulty}[/dim]")
            info_parts.append(f"[dim]ID: {machine_id}[/dim]")

            progress_bar = ProgressBar(total=total_count, completed=completed_count, width=40)

            header_content = Group(
                Text.from_markup(" | ".join(info_parts)),
                Text(""),
                Group(
                    progress_bar,
                    Text.from_markup(f"  {completed_count}/{total_count} tasks  {status_label}"),
                ),
                Text(""),
                Text.from_markup(f"[dim]user/root flag: htbcli machines submit-task {machine_identifier} <flag>[/dim]"),
                Text.from_markup(f"[dim]task answer:   htbcli machines submit-task {machine_identifier} --task <id> <answer>[/dim]"),
            )

            console.print(Panel(
                header_content,
                title="[bold cyan]GUIDED MODE[/bold cyan]",
                border_style="cyan",
                padding=(1, 2),
            ))
            console.print()

        # --- Build a prereq map for display: task_id -> step number ---
        id_to_step = {}
        for idx, step in enumerate(steps, 1):
            if step.get('id') is not None:
                id_to_step[step['id']] = idx

        # --- Categorize steps into sections ---
        # Group: task questions before user flag, user flag, task questions before root, root flag
        sections = []
        current_section_tasks = []
        for step in steps:
            type_text = step.get('type', {}).get('text', 'task') if isinstance(step.get('type'), dict) else 'task'
            if type_text in ('user', 'root'):
                if current_section_tasks:
                    sections.append(('tasks', current_section_tasks))
                    current_section_tasks = []
                sections.append(('flag', [step]))
            else:
                current_section_tasks.append(step)
        if current_section_tasks:
            sections.append(('tasks', current_section_tasks))

        step_num = 0
        for section_type, section_steps in sections:
            if section_type == 'tasks':
                # --- Task questions section ---
                # Determine section label based on what comes after
                section_idx = sections.index((section_type, section_steps))
                if section_idx + 1 < len(sections):
                    next_section = sections[section_idx + 1]
                    if next_section[0] == 'flag':
                        flag_type = next_section[1][0].get('type', {}).get('text', '')
                        if flag_type == 'user':
                            section_title = "ENUMERATION & EXPLOITATION"
                        elif flag_type == 'root':
                            section_title = "PRIVILEGE ESCALATION"
                        else:
                            section_title = "TASKS"
                    else:
                        section_title = "TASKS"
                else:
                    section_title = "TASKS"

                console.print(Rule(f"[bold]{section_title}[/bold]", style="dim"))
                console.print()

                for step in section_steps:
                    step_num += 1
                    completed = step.get('completed', False)
                    title = step.get('title', 'Untitled')
                    description = step.get('description', '')
                    hint = step.get('hint', '')
                    masked_flag = step.get('masked_flag', '')
                    prereq_id = step.get('prerequisite_id')
                    task_id = step.get('id')

                    # Status indicator
                    if completed:
                        status_icon = "[bold green]  [/bold green]"
                        num_style = "green"
                        title_markup = f"[green]{title}[/green]"
                    else:
                        status_icon = "[bold red]  [/bold red]"
                        num_style = "bold white"
                        title_markup = f"[bold white]{title}[/bold white]"

                    # Step number badge
                    step_header = Text.from_markup(
                        f" {status_icon} [{num_style}]{step_num:>2}[/{num_style}]  {title_markup}"
                    )
                    console.print(step_header)

                    # Description
                    if description:
                        console.print(Text.from_markup(f"        [italic]{description}[/italic]"))

                    # Metadata line
                    meta_parts = []
                    if masked_flag:
                        meta_parts.append(f"[cyan]Flag: {masked_flag}[/cyan]")
                    if prereq_id is not None and prereq_id in id_to_step:
                        meta_parts.append(f"[dim]After step {id_to_step[prereq_id]}[/dim]")
                    if task_id:
                        meta_parts.append(f"[dim]#{task_id}[/dim]")
                    if meta_parts:
                        console.print(Text.from_markup("        " + "  |  ".join(meta_parts)))

                    # Hint
                    if hint and not completed:
                        if show_hints:
                            console.print(Text.from_markup(f"        [yellow]Hint:[/yellow] [dim italic]{hint}[/dim italic]"))
                        else:
                            console.print(Text.from_markup("        [dim]Hint available (--show-hints)[/dim]"))

                    console.print()

            elif section_type == 'flag':
                # --- Flag submission step ---
                for step in section_steps:
                    step_num += 1
                    completed = step.get('completed', False)
                    title = step.get('title', 'Untitled')
                    description = step.get('description', '')
                    masked_flag = step.get('masked_flag', '')
                    type_text = step.get('type', {}).get('text', '') if isinstance(step.get('type'), dict) else ''

                    if type_text == 'user':
                        flag_icon = "👤"
                        flag_color = "magenta"
                    else:
                        flag_icon = "💀"
                        flag_color = "red"

                    if completed:
                        border_style = "green"
                        status_text = "[bold green]  OWNED[/bold green]"
                    else:
                        border_style = flag_color
                        status_text = f"[bold {flag_color}]  PENDING[/bold {flag_color}]"

                    flag_lines = [f"{flag_icon}  {status_text}"]
                    if description:
                        flag_lines.append(f"   [italic]{description}[/italic]")
                    if masked_flag:
                        flag_lines.append(f"   [dim]Format:[/dim] [cyan]{masked_flag}[/cyan]")

                    console.print(Panel(
                        "\n".join(flag_lines),
                        title=f"[bold {flag_color}]Step {step_num}: {title}[/bold {flag_color}]",
                        border_style=border_style,
                        padding=(0, 2),
                    ))
                    console.print()

        # --- Footer ---
        if completed_count == total_count and total_count > 0:
            console.print(Panel(
                "[bold green]All tasks completed! Machine fully owned![/bold green]",
                border_style="green",
                padding=(0, 2),
            ))
        elif completed_count > 0 or completed_count == 0:
            next_task = next((s for s in steps if not s.get('completed')), None)
            if next_task:
                next_title = next_task.get('title', 'Unknown')
                next_desc = next_task.get('description', '')
                next_flag = next_task.get('masked_flag', '')
                footer_lines = [f"[bold cyan]Next:[/bold cyan] {next_title}"]
                if next_desc:
                    footer_lines.append(f"[dim]{next_desc}[/dim]")
                if next_flag:
                    footer_lines.append(f"[dim]Expected: [cyan]{next_flag}[/cyan][/dim]")
                console.print(Panel(
                    "\n".join(footer_lines),
                    border_style="dim cyan",
                    padding=(0, 2),
                ))

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command(name='submit-task')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
@click.option('--task', 'task_id', type=int, default=None,
              help='Task ID for guided-mode question answers (from `machines tasks` ID column). '
                   'Omit to submit a user/root flag via the standard /own endpoint.')
@click.argument('machine_identifier', required=False)
@click.argument('flag', required=False)
def submit_task(machine_identifier, flag, debug, json_output, task_id):
    """Submit answer/flag for a guided-mode task. Uses active machine if none specified. Flag can be piped from stdin."""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)

        # Handle argument parsing - if only one argument is provided, it's the flag
        if machine_identifier is not None and flag is None:
            flag = machine_identifier
            machine_identifier = None

        # Determine machine ID
        machine_id = None
        if machine_identifier is None:
            machine_id = machines_module.get_active_machine_id()
            if machine_id is None:
                console.print("[red]No machine specified and no active machine found[/red]")
                return
        else:
            machine_id = machines_module.resolve_machine_id(machine_identifier)
            if machine_id is None:
                console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
                return

        # Get flag from argument or stdin
        if flag is None:
            if not sys.stdin.isatty():
                flag = sys.stdin.read().strip()
                if not flag:
                    console.print("[red]No flag provided via stdin[/red]")
                    return
            else:
                console.print("[red]No flag provided. Use: htbcli machines submit-task [machine] <flag>[/red]")
                return

        # Get tasks before submission to track progress
        tasks_before = machines_module.get_machines_tasks(machine_id)
        pending_before = set()
        if tasks_before and 'data' in tasks_before:
            pending_before = {t['id'] for t in tasks_before['data'] if not t.get('completed') and t.get('id')}

        # Submit via per-task endpoint if --task was given, otherwise fall back to /own
        if task_id is not None:
            result = machines_module.submit_machine_task_flag(machine_id, task_id, flag)
        else:
            result = machines_module.submit_machine_flag(flag, machine_id)

        if handle_debug_option(debug, result, f"Debug: Task Flag Submission (Machine ID: {machine_id})", json_output):
            return

        if result:
            message = result.get('message', 'N/A')
            console.print(Panel.fit(
                f"[bold green]Flag Submission Result[/bold green]\n"
                f"Machine ID: {machine_id}\n"
                f"Message: {message}",
                title="Task Flag Submission",
                border_style="green"
            ))

            # Check which task was completed by comparing before/after
            tasks_after = machines_module.get_machines_tasks(machine_id)
            if tasks_after and 'data' in tasks_after:
                tasks_data = tasks_after['data']
                completed_now = {t['id'] for t in tasks_data if t.get('completed') and t.get('id')}
                newly_completed = completed_now & pending_before

                if newly_completed:
                    for task in tasks_data:
                        if task.get('id') in newly_completed:
                            console.print(f"[green]✓[/green] Completed task: [bold]{task.get('title', 'Unknown')}[/bold]")

                completed_count = sum(1 for t in tasks_data if t.get('completed'))
                total_count = len(tasks_data)
                console.print(f"\n[cyan]Progress: {completed_count}/{total_count} tasks completed[/cyan]")

                if completed_count == total_count and total_count > 0:
                    console.print("[bold green]🎉 All tasks completed! Machine fully owned![/bold green]")
                else:
                    next_task = next((t for t in tasks_data if not t.get('completed')), None)
                    if next_task:
                        console.print(f"[cyan]Next task:[/cyan] {next_task.get('title', 'Unknown')}")
                        if next_task.get('masked_flag'):
                            console.print(f"[dim]Expected flag format: {next_task.get('masked_flag')}[/dim]")
        else:
            console.print("[yellow]No result from flag submission[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
