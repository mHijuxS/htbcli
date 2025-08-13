"""
Machines module for HTB CLI
"""

import click
import sys
from typing import Dict, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option
from .vpn import VPNModule

console = Console()

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
    
    def get_machine_list_retired_paginated(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated list of retired machines"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/machine/list/retired/paginated", params=params)
    
    def submit_machine_flag(self, flag: str, machine_id: int) -> Dict[str, Any]:
        """Submit flag for machine"""
        # Use v5 API for flag submission with both flag and machine ID
        v5_api_client = HTBAPIClient(version="v5")
        return v5_api_client.post("/machine/own", json_data={"flag": flag, "id": machine_id})
    
    def get_machine_owns_top(self, machine_id: int) -> Dict[str, Any]:
        """Get top 25 owners for a machine"""
        return self.api.get(f"/machine/owns/top/{machine_id}")
    
    def get_machine_paginated(self, page: int = 1, per_page: int = 20, status: Optional[str] = None) -> Dict[str, Any]:
        """Get paginated list of machines"""
        params = {
            "page": page,
            "per_page": per_page
        }
        if status:
            params["status"] = status
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
    
    def get_machine_writeup(self, machine_id: int) -> Dict[str, Any]:
        """Get machine writeup"""
        return self.api.get(f"/machine/writeup/{machine_id}")
    
    def get_machines_adventure(self, machine_id: int) -> Dict[str, Any]:
        """Get machines adventure"""
        return self.api.get(f"/machines/adventure/{machine_id}")
    
    def get_machines_tasks(self, machine_id: int) -> Dict[str, Any]:
        """Get machines tasks"""
        return self.api.get(f"/machines/tasks/{machine_id}")
    
    def search_machine_by_name(self, machine_name: str, max_pages: int = 5) -> Optional[int]:
        """Search for a machine by name and return its ID"""
        try:
            # Search through multiple pages to find the machine
            for page in range(1, max_pages + 1):
                result = self.get_machine_paginated(page=page, per_page=20, status='active')
                
                if not result or 'data' not in result:
                    continue
                
                machines = result['data']
                if not machines:
                    continue
                
                # Search through machines on this page
                for machine in machines:
                    name = machine.get('name', '').lower()
                    machine_id = machine.get('id')
                    
                    # Check for exact match first
                    if name == machine_name.lower():
                        return machine_id
                    
                    # Check for partial match (contains)
                    if machine_name.lower() in name:
                        return machine_id
                
                # If no more machines on this page, stop searching
                if len(machines) < 20:
                    break
            
            return None
            
        except Exception as e:
            console.print(f"[red]Error searching for machine '{machine_name}': {e}[/red]")
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
def active(debug):
    """Get currently active machine and VM status"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_vm_status()
        
        if handle_debug_option(debug, result, "Debug: Active Machine API Response"):
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

@click.argument('machine_identifier')
def activity(machine_identifier, debug):
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
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"Machine Activity (ID: {machine_id})")
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

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('machine_identifier')
def changelog(machine_identifier, debug):
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

@click.argument('machine_identifier')
def creators(machine_identifier, debug):
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
                        str(creator.get('avatar', 'N/A') or 'N/A'),
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
@click.option('--status', default='active', help='Machine status (active/retired)')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_machines(page, per_page, status, responses, option):
    """List machines"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        if status == 'retired':
            result = machines_module.get_machine_list_retired_paginated(page, per_page)
        else:
            result = machines_module.get_machine_paginated(page, per_page, status)
        
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
                table.add_column("Points", style="blue")
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
                        str(machine.get('difficulty', 'N/A') or 'N/A'),
                        str(machine.get('points', 'N/A') or 'N/A'),
                        str(machine.get('status', 'N/A') or 'N/A')
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
                table.add_column("Points", style="blue")
                table.add_column("Status", style="red")
                
                try:
                    for machine in machines_data:
                        table.add_row(
                            str(machine.get('id', 'N/A') or 'N/A'),
                            str(machine.get('name', 'N/A') or 'N/A'),
                            str(machine.get('os', 'N/A') or 'N/A'),
                            str(machine.get('difficulty', 'N/A') or 'N/A'),
                            str(machine.get('points', 'N/A') or 'N/A'),
                            str(machine.get('status', 'N/A') or 'N/A')
                        )
                    
                    console.print(table)
                except Exception as e:
                    console.print(f"[yellow]Error processing machines data: {e}[/yellow]")
        else:
            console.print("[yellow]No machines found[/yellow]")
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
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for Machine Profile[/bold green]\n"
                    f"{chr(10).join([f'{k}: {v}' for k, v in info.items()])}",
                    title=f"Machine: {machine_slug} - All Fields"
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
                        title=f"Machine: {machine_slug} - Selected Fields"
                    ))
            else:
                # Default view with enhanced information
                maker_name = info.get('maker', {}).get('name', 'N/A') if info.get('maker') else 'N/A'
                difficulty_text = info.get('difficultyText', 'N/A')
                stars = info.get('stars', 'N/A')
                is_guided = 'Yes' if info.get('isGuidedEnabled') else 'No'
                auth_user_owns = 'Yes' if info.get('authUserInUserOwns') else 'No'
                auth_root_owns = 'Yes' if info.get('authUserInRootOwns') else 'No'
                
                console.print(Panel.fit(
                    f"[bold green]Machine Profile[/bold green]\n"
                    f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                    f"OS: {info.get('os', 'N/A') or 'N/A'}\n"
                    f"Difficulty: {difficulty_text}\n"
                    f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                    f"Stars: {stars}\n"
                    f"Status: {'Active' if info.get('active') else 'Retired' if info.get('retired') else 'N/A'}\n"
                    f"IP: {info.get('ip', 'N/A') or 'N/A'}\n"
                    f"User Owns: {info.get('user_owns_count', 'N/A') or 'N/A'}\n"
                    f"Root Owns: {info.get('root_owns_count', 'N/A') or 'N/A'}\n"
                    f"Maker: {maker_name}\n"
                    f"Guided Mode: {is_guided}\n"
                    f"You Own User: {auth_user_owns}\n"
                    f"You Own Root: {auth_root_owns}\n"
                    f"Release Date: {info.get('release', 'N/A') or 'N/A'}",
                    title=f"Machine: {machine_slug}"
                ))
        else:
            console.print("[yellow]Machine not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('machine_identifier', required=False)
@click.argument('flag', required=False)
def submit(machine_identifier, flag, debug):
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

def recommended(debug):
    """Get recommended machines"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_recommended()
        
        if handle_debug_option(debug, result, "Debug: Recommended Machines API Response"):
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

def tags(debug):
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
def unreleased(debug):
    """Get unreleased machines"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_unreleased()
        
        if debug:
            console.print(Panel.fit(
                f"[bold green]Raw API Response[/bold green]\n"
                f"{result}",
                title="Debug: Unreleased Machines API Response"
            ))
            return
        
        if result and 'data' in result:
            unreleased_data = result['data']
            
            table = Table(title="Unreleased Machines")
            table.add_column("Name", style="cyan")
            table.add_column("OS", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Release Date", style="magenta")
            table.add_column("Creators", style="blue")
            
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
                
                table.add_row(
                    str(machine.get('name', 'N/A') or 'N/A'),
                    str(machine.get('os', 'N/A') or 'N/A'),
                    str(difficulty),
                    str(release_date),
                    creators_str
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

@click.argument('machine_identifier')
def graph_matrix(machine_identifier, debug):
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

@click.argument('machine_identifier')
def graph_difficulty(machine_identifier, debug):
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
def retired_list(page, per_page):
    """Get paginated list of retired machines"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_list_retired_paginated(page, per_page)
        
        if result and 'data' in result:
            machines_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Retired Machines (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("OS", style="yellow")
            table.add_column("Difficulty", style="magenta")
            table.add_column("Points", style="blue")
            
            for machine in machines_data:
                table.add_row(
                    str(machine.get('id', 'N/A') or 'N/A'),
                    str(machine.get('name', 'N/A') or 'N/A'),
                    str(machine.get('os', 'N/A') or 'N/A'),
                    str(machine.get('difficulty', 'N/A') or 'N/A'),
                    str(machine.get('points', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No retired machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('machine_identifier')
def owns_top(machine_identifier, debug):
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
            
            table = Table(title=f"Top Owners for Machine (ID: {machine_id})")
            table.add_column("Position", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Rank", style="yellow")
            table.add_column("User Own Time", style="magenta")
            table.add_column("Root Own Time", style="blue")
            
            for owner in owners_data:
                table.add_row(
                    str(owner.get('position', 'N/A') or 'N/A'),
                    str(owner.get('name', 'N/A') or 'N/A'),
                    str(owner.get('rank_text', 'N/A') or 'N/A'),
                    str(owner.get('user_own_time', 'N/A') or 'N/A'),
                    str(owner.get('root_own_time', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No owners data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

def recommended_retired(debug):
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

@click.argument('machine_identifier')
def reviews(machine_identifier, debug):
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

@click.argument('machine_identifier')
def reviews_user(machine_identifier, debug):
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

@click.argument('machine_identifier')
def machine_tags(machine_identifier, debug):
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
            table.add_column("Points", style="blue")
            
            for machine in todo_data:
                table.add_row(
                    str(machine.get('id', 'N/A') or 'N/A'),
                    str(machine.get('name', 'N/A') or 'N/A'),
                    str(machine.get('os', 'N/A') or 'N/A'),
                    str(machine.get('difficulty', 'N/A') or 'N/A'),
                    str(machine.get('points', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No todo machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

def walkthrough_random(debug):
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

def walkthrough_languages(debug):
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

def walkthrough_feedback_choices(debug):
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

@click.argument('machine_identifier')
def walkthroughs(machine_identifier, debug):
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

@click.argument('machine_identifier')
def writeup(machine_identifier, debug):
    """Get machine writeup (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machine_writeup(machine_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Machine Writeup[/bold green]\n"
                f"Machine ID: {machine_id}\n"
                f"Data: {result}",
                title="Machine Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('machine_identifier')
def adventure(machine_identifier, debug):
    """Get machine adventure (accepts machine ID or name)"""
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        
        # Resolve machine identifier to machine ID
        machine_id = machines_module.resolve_machine_id(machine_identifier)
        if machine_id is None:
            console.print(f"[red]Could not resolve machine identifier: {machine_identifier}[/red]")
            return
        
        result = machines_module.get_machines_adventure(machine_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Machine Adventure[/bold green]\n"
                f"Machine ID: {machine_id}\n"
                f"Data: {result}",
                title="Machine Adventure"
            ))
        else:
            console.print("[yellow]No adventure data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')

@click.argument('machine_identifier')
def tasks(machine_identifier, debug):
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
        
        if result and 'data' in result:
            tasks_data = result['data']
            
            table = Table(title=f"Machine Tasks (ID: {machine_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Description", style="yellow")
            table.add_column("Points", style="magenta")
            
            for task in tasks_data:
                table.add_row(
                    str(task.get('id', 'N/A') or 'N/A'),
                    str(task.get('title', 'N/A') or 'N/A'),
                    str(task.get('description', 'N/A') or 'N/A'),
                    str(task.get('points', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No tasks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
