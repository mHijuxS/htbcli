"""
Prolabs module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

class ProlabsModule:
    """Module for handling ProLab-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    # Valid endpoints from OpenAPI specification
    def get_prolabs(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get list of prolabs"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/prolabs", params=params)
    
    def get_prolab_changelogs(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab changelog"""
        return self.api.get(f"/prolab/{prolab_id}/changelogs")
    
    def get_prolab_faq(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab FAQ"""
        return self.api.get(f"/prolab/{prolab_id}/faq")
    
    def submit_prolab_flag(self, prolab_id: int, flag: str) -> Dict[str, Any]:
        """Submit prolab flag"""
        return self.api.post(f"/prolab/{prolab_id}/flag", json_data={"flag": flag})
    
    def get_prolab_flags(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab flags"""
        return self.api.get(f"/prolab/{prolab_id}/flags")
    
    def get_prolab_info(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab info by ID"""
        return self.api.get(f"/prolab/{prolab_id}/info")
    
    def get_prolab_machines(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab machines"""
        return self.api.get(f"/prolab/{prolab_id}/machines")
    
    def get_prolab_overview(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab overview"""
        return self.api.get(f"/prolab/{prolab_id}/overview")
    
    def get_prolab_progress(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab progress"""
        return self.api.get(f"/prolab/{prolab_id}/progress")
    
    def get_prolab_rating(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab rating"""
        return self.api.get(f"/prolab/{prolab_id}/rating")
    
    def get_prolab_reviews(self, prolab_id: int, page: int = 1) -> Dict[str, Any]:
        """Get prolab reviews"""
        params = {"page": page}
        return self.api.get(f"/prolab/{prolab_id}/reviews", params=params)
    
    def get_prolab_reviews_overview(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab reviews overview"""
        return self.api.get(f"/prolab/{prolab_id}/reviews_overview")
    
    def get_prolab_subscription(self, prolab_id: int) -> Dict[str, Any]:
        """Get prolab subscription"""
        return self.api.get(f"/prolab/{prolab_id}/subscription")
    
    def resolve_prolab_identifier_to_id(self, identifier: str) -> Optional[int]:
        """Resolve prolab identifier/slug to numeric ID"""
        # Get all prolabs to find the matching identifier
        result = self.get_prolabs()
        if result and 'data' in result and 'labs' in result['data']:
            labs = result['data']['labs']
            identifier_lower = identifier.lower()
            
            for lab in labs:
                # Check both identifier and name (case-insensitive)
                lab_identifier = lab.get('identifier', '').lower()
                lab_name = lab.get('name', '').lower()
                
                if lab_identifier == identifier_lower or lab_name == identifier_lower:
                    return lab.get('id')
        
        return None

# Click commands
@click.group()
def prolabs():
    """ProLab-related commands"""
    pass

@prolabs.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_prolabs(page, per_page, responses, option):
    """List prolabs"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        result = prolabs_module.get_prolabs(page, per_page)
        
        if result and 'data' in result:
            prolabs_data = result['data']['labs'] if isinstance(result['data'], dict) and 'labs' in result['data'] else result['data']
            
            if responses:
                # Show all available fields for first prolab
                if prolabs_data:
                    first_prolab = prolabs_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for ProLabs[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_prolab.items()])}",
                        title=f"ProLabs - All Fields (First Item, Page {page})"
                    ))
            elif option:
                # Show default table with additional specified fields
                table = Table(title=f"ProLabs (Page {page})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Skill Level", style="yellow")
                table.add_column("Flags", style="magenta")
                table.add_column("State", style="blue")
                table.add_column("Machines", style="red")
                
                # Add additional columns for specified fields
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for prolab in prolabs_data:
                    # Default row data
                    row = [
                        str(prolab.get('id', 'N/A') or 'N/A'),
                        str(prolab.get('name', 'N/A') or 'N/A'),
                        str(prolab.get('skill_level', 'N/A') or 'N/A'),
                        str(prolab.get('pro_flags_count', 'N/A') or 'N/A'),
                        str(prolab.get('state', 'N/A') or 'N/A'),
                        str(prolab.get('pro_machines_count', 'N/A') or 'N/A')
                    ]
                    
                    # Add additional specified fields
                    for field in option:
                        row.append(str(prolab.get(field, 'N/A') or 'N/A'))
                    
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title=f"ProLabs (Page {page})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Skill Level", style="yellow")
                table.add_column("Flags", style="magenta")
                table.add_column("State", style="blue")
                table.add_column("Machines", style="red")
                
                try:
                    for prolab in prolabs_data:
                        table.add_row(
                            str(prolab.get('id', 'N/A') or 'N/A'),
                            str(prolab.get('name', 'N/A') or 'N/A'),
                            str(prolab.get('skill_level', 'N/A') or 'N/A'),
                            str(prolab.get('pro_flags_count', 'N/A') or 'N/A'),
                            str(prolab.get('state', 'N/A') or 'N/A'),
                            str(prolab.get('pro_machines_count', 'N/A') or 'N/A')
                        )
                    
                    console.print(table)
                except Exception as e:
                    console.print(f"[yellow]Error processing prolabs data: {e}[/yellow]")
        else:
            console.print("[yellow]No prolabs found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('prolab_identifier')
def info(prolab_identifier, debug, json_output):
    """Get prolab info by identifier/name"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        result = prolabs_module.get_prolab_info(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Info", json_output)
            return
        
        if result and 'data' in result:
            info = result['data']
            
            # Get lab masters names
            lab_masters = info.get('lab_masters', [])
            masters_names = ', '.join([master.get('name', 'Unknown') for master in lab_masters]) if lab_masters else 'N/A'
            
            console.print(Panel.fit(
                f"[bold green]ProLab Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"ID: {info.get('id', 'N/A') or 'N/A'}\n"
                f"Identifier: {info.get('identifier', 'N/A') or 'N/A'}\n"
                f"Version: {info.get('version', 'N/A') or 'N/A'}\n"
                f"Flags: {info.get('pro_flags_count', 'N/A') or 'N/A'}\n"
                f"State: {info.get('state', 'N/A') or 'N/A'}\n"
                f"Machines: {info.get('pro_machines_count', 'N/A') or 'N/A'}\n"
                f"Lab Servers: {info.get('lab_servers_count', 'N/A') or 'N/A'}\n"
                f"Active Users: {info.get('active_users', 'N/A') or 'N/A'}\n"
                f"Lab Masters: {masters_names}\n"
                f"Entry Points: {', '.join(info.get('entry_points', [])) if info.get('entry_points') else 'N/A'}\n"
                f"Mini Lab: {'Yes' if info.get('mini') else 'No'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"ProLab: {prolab_identifier}"
            ))
        else:
            console.print("[yellow]ProLab info not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def overview(prolab_identifier, debug, json_output):
    """Get prolab overview"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        result = prolabs_module.get_prolab_overview(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Overview", json_output)
            return
        
        if result and 'data' in result:
            overview_data = result['data']
            
            # Get lab masters names
            lab_masters = overview_data.get('lab_masters', [])
            masters_names = ', '.join([master.get('name', 'Unknown') for master in lab_masters]) if lab_masters else 'N/A'
            
            # Get designated level info
            designated_level = overview_data.get('designated_level', {})
            level_info = f"{designated_level.get('category', 'N/A')} Level {designated_level.get('level', 'N/A')}" if designated_level else 'N/A'
            
            console.print(Panel.fit(
                f"[bold green]ProLab Overview[/bold green]\n"
                f"Name: {overview_data.get('name', 'N/A') or 'N/A'}\n"
                f"Version: {overview_data.get('version', 'N/A') or 'N/A'}\n"
                f"Skill Level: {overview_data.get('skill_level', 'N/A') or 'N/A'}\n"
                f"Designated Level: {level_info}\n"
                f"State: {overview_data.get('state', 'N/A') or 'N/A'}\n"
                f"Mini Lab: {'Yes' if overview_data.get('mini') else 'No'}\n"
                f"Machines: {overview_data.get('pro_machines_count', 'N/A') or 'N/A'}\n"
                f"Flags: {overview_data.get('pro_flags_count', 'N/A') or 'N/A'}\n"
                f"Lab Masters: {masters_names}\n"
                f"Eligible to Play: {'Yes' if overview_data.get('user_eligible_to_play') else 'No'}\n"
                f"New Version: {'Yes' if overview_data.get('new_version') else 'No'}",
                title=f"ProLab Overview: {prolab_identifier}"
            ))
        else:
            console.print("[yellow]ProLab overview not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def changelogs(prolab_identifier, debug, json_output):
    """Get prolab changelogs"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        result = prolabs_module.get_prolab_changelogs(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Changelogs", json_output)
            return
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            table = Table(title=f"ProLab Changelogs: {prolab_identifier}")
            table.add_column("Date", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Title", style="yellow")
            table.add_column("Author", style="magenta")
            table.add_column("Description", style="blue")
            
            for change in changelog_data:
                user_name = change.get('user', {}).get('name', 'N/A') if change.get('user') else 'N/A'
                table.add_row(
                    str(change.get('created_at', 'N/A') or 'N/A'),
                    str(change.get('type', 'N/A') or 'N/A'),
                    str(change.get('title', 'N/A') or 'N/A'),
                    user_name,
                    str(change.get('description', 'N/A') or 'N/A')[:100] + "..." if len(str(change.get('description', ''))) > 100 else str(change.get('description', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No changelog found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")



@prolabs.command()
@click.argument('prolab_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def machines(prolab_identifier, debug, json_output):
    """Get prolab machines"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        result = prolabs_module.get_prolab_machines(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Machines", json_output)
            return
        
        if result and 'data' in result:
            machines_data = result['data']
            
            table = Table(title=f"ProLab Machines: {prolab_identifier}")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("OS", style="yellow")
            
            for machine in machines_data:
                table.add_row(
                    str(machine.get('id', 'N/A') or 'N/A'),
                    str(machine.get('name', 'N/A') or 'N/A'),
                    str(machine.get('os', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def progress(prolab_identifier, debug, json_output):
    """Get prolab progress"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        result = prolabs_module.get_prolab_progress(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Progress", json_output)
            return
        
        if result and 'data' in result:
            progress_data = result['data']
            
            # Get milestone information
            milestones = progress_data.get('keyed_pro_lab_mile_stone', [])
            milestone_text = ""
            for milestone in milestones:
                status = "✓" if milestone.get('isMilestoneReached') else "✗"
                milestone_text += f"{status} {milestone.get('text', 'N/A')} ({milestone.get('percent', 'N/A')}%)\n"
            
            console.print(Panel.fit(
                f"[bold green]ProLab Progress[/bold green]\n"
                f"Ownership: {progress_data.get('ownership', 'N/A') or 'N/A'}%\n"
                f"Required for Certification: {progress_data.get('ownership_required_for_certification', 'N/A') or 'N/A'}%\n"
                f"Eligible for Certificate: {'Yes' if progress_data.get('user_eligible_for_certificate') else 'No'}\n\n"
                f"[bold]Milestones:[/bold]\n{milestone_text}",
                title=f"ProLab Progress: {prolab_identifier}"
            ))
        else:
            console.print("[yellow]No progress data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_identifier')
@click.option('--page', default=1, help='Page number')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def reviews(prolab_identifier, page, debug, json_output):
    """Get prolab reviews"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        result = prolabs_module.get_prolab_reviews(prolab_id, page)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Reviews", json_output)
            return
        
        if result and 'data' in result:
            reviews_data = result['data']
            
            table = Table(title=f"ProLab Reviews: {prolab_identifier} (Page {page})")
            table.add_column("User", style="cyan")
            table.add_column("Rating", style="green")
            table.add_column("Difficulty", style="blue")
            table.add_column("Review", style="yellow")
            table.add_column("Date", style="magenta")
            
            for review in reviews_data:
                user_name = review.get('user', {}).get('name', 'N/A') if review.get('user') else 'N/A'
                table.add_row(
                    user_name,
                    str(review.get('rating', 'N/A') or 'N/A'),
                    str(review.get('difficulty', 'N/A') or 'N/A'),
                    str(review.get('text', 'N/A') or 'N/A')[:100] + "..." if len(str(review.get('text', ''))) > 100 else str(review.get('text', 'N/A') or 'N/A'),
                    str(review.get('created_at', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No reviews found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_identifier')
@click.argument('flag')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def submit_flag(prolab_identifier, flag, debug, json_output):
    """Submit a flag for a prolab"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        result = prolabs_module.submit_prolab_flag(prolab_id, flag)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: Flag Submission", json_output)
            return
        
        if result and 'status' in result:
            if result['status']:
                console.print(f"[green]✓ Flag submitted successfully for {prolab_identifier}![/green]")
            else:
                message = result.get('message', 'Unknown error')
                console.print(f"[red]✗ Flag submission failed: {message}[/red]")
        else:
            console.print("[yellow]Unexpected response format[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def flags(prolab_identifier, debug, json_output):
    """Get prolab flags"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        result = prolabs_module.get_prolab_flags(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            handle_debug_option(debug, result, "Debug: ProLab Flags", json_output)
            return
        
        if result and 'data' in result:
            flags_data = result['data']
            
            table = Table(title=f"ProLab Flags: {prolab_identifier}")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Points", style="yellow")
            table.add_column("Owned", style="magenta")
            
            for flag in flags_data:
                table.add_row(
                    str(flag.get('id', 'N/A') or 'N/A'),
                    str(flag.get('title', 'N/A') or 'N/A'),
                    str(flag.get('points', 'N/A') or 'N/A'),
                    "✓" if flag.get('owned') else "✗"
                )
            
            console.print(table)
        else:
            console.print("[yellow]No flags found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@prolabs.command()
@click.argument('prolab_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def connection(prolab_identifier, debug, json_output):
    """Get prolab connection information"""
    try:
        api_client = HTBAPIClient()
        prolabs_module = ProlabsModule(api_client)
        
        # Resolve identifier to ID
        prolab_id = prolabs_module.resolve_prolab_identifier_to_id(prolab_identifier)
        if prolab_id is None:
            console.print(f"[yellow]ProLab '{prolab_identifier}' not found[/yellow]")
            return
        
        # Import connection module
        from ..modules.connection import ConnectionModule
        connection_module = ConnectionModule(api_client)
        
        # Get connection status
        status_result = connection_module.get_connection_status_prolab(prolab_id)
        
        if debug:
            from ..base_command import handle_debug_option
            console.print(f"[bold]Debug: ProLab Connection Status for {prolab_identifier} (ID: {prolab_id})[/bold]")
            handle_debug_option(debug, status_result, "Debug: Connection Status", json_output)
            return
        
        # Display connection status
        if status_result and 'data' in status_result:
            status_data = status_result['data']
            
            # Extract server information
            server_info = status_data.get('server', {})
            if isinstance(server_info, dict):
                server_name = server_info.get('friendly_name', 'N/A')
                server_hostname = server_info.get('hostname', 'N/A')
                server_id = server_info.get('id', 'N/A')
            else:
                server_name = str(server_info) if server_info else 'N/A'
                server_hostname = 'N/A'
                server_id = 'N/A'
            
            console.print(Panel.fit(
                f"[bold green]ProLab Connection Status[/bold green]\n"
                f"ProLab: {prolab_identifier} (ID: {prolab_id})\n"
                f"Connected: {status_data.get('connected', 'N/A') or 'N/A'}\n"
                f"Server ID: {server_id}\n"
                f"Server Name: {server_name}\n"
                f"Server Hostname: {server_hostname}\n"
                f"IP: {status_data.get('ip', 'N/A') or 'N/A'}",
                title=f"ProLab Connection: {prolab_identifier}"
            ))
        elif status_result and 'status' in status_result and not status_result['status']:
            # Handle API error responses
            message = status_result.get('message', 'Unknown error')
            console.print(Panel.fit(
                f"[bold yellow]ProLab Connection Status[/bold yellow]\n"
                f"ProLab: {prolab_identifier} (ID: {prolab_id})\n"
                f"Status: Not Connected\n"
                f"Message: {message}",
                title=f"ProLab Connection: {prolab_identifier}"
            ))
        else:
            console.print("[yellow]No connection status found[/yellow]")
        
        # Get available servers
        servers_result = connection_module.get_connections_servers_prolab(prolab_id)
        
        if servers_result and 'data' in servers_result:
            data = servers_result['data']
            
            # Show assigned server
            if 'assigned' in data and data['assigned']:
                assigned = data['assigned']
                console.print(Panel.fit(
                    f"[bold green]Currently Assigned Server[/bold green]\n"
                    f"ID: {assigned.get('id', 'N/A') or 'N/A'}\n"
                    f"Name: {assigned.get('friendly_name', 'N/A') or 'N/A'}\n"
                    f"Location: {assigned.get('location', 'N/A') or 'N/A'}\n"
                    f"Current Clients: {assigned.get('current_clients', 'N/A') or 'N/A'}",
                    title="Assigned Server"
                ))
            
            # Show available servers summary
            if 'options' in data and data['options']:
                console.print("\n[bold]Available Server Locations:[/bold]")
                
                for region, region_data in data['options'].items():
                    for location_name, location_data in region_data.items():
                        servers = location_data.get('servers', {})
                        server_count = len(servers)
                        available_count = sum(1 for s in servers.values() if not s.get('full', False))
                        
                        console.print(f"  • {location_name} ({location_data.get('location', 'N/A')}): {available_count}/{server_count} servers available")
            else:
                console.print("[yellow]No server options available[/yellow]")
        else:
            console.print("[yellow]No server information found[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
