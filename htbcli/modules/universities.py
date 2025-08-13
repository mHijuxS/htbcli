"""
Universities module for HTB CLI
"""

import click
from typing import Dict, Any, Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

class UniversitiesModule:
    """Module for handling university ranking-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_university_activity(self, university_id: int) -> Dict[str, Any]:
        """Get university activity"""
        return self.api.get(f"/university/activity/{university_id}")
    
    def get_university_all_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get paginated list of all universities"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/university/all/list", params=params)
    
    def get_university_chart_challenge_categories(self, university_id: int) -> Dict[str, Any]:
        """Get university challenge categories chart"""
        return self.api.get(f"/university/chart/challenge/categories/{university_id}")
    
    def get_university_chart_machines_attack(self, university_id: int) -> Dict[str, Any]:
        """Get university machine attack chart"""
        return self.api.get(f"/university/chart/machines/attack/{university_id}")
    
    def get_university_country_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get university country list"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/university/country/list", params=params)
    
    def get_university_members(self, university_id: int) -> Dict[str, Any]:
        """Get university members"""
        return self.api.get(f"/university/members/{university_id}")
    
    def get_university_new_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get university new list"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/university/new/list", params=params)
    
    def get_university_profile(self, university_id: int) -> Dict[str, Any]:
        """Get university profile by ID"""
        return self.api.get(f"/university/profile/{university_id}")
    
    def get_university_stats_owns(self, user_id: int) -> Dict[str, Any]:
        """Get university owns statistics for a user"""
        return self.api.get(f"/university/stats/owns/{user_id}")
    
    def get_university_top_list(self, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Get university top list"""
        params = {
            "page": page,
            "per_page": per_page
        }
        return self.api.get("/university/top/list", params=params)

# Click commands
@click.group()
def universities():
    """University ranking-related commands"""
    pass

@universities.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_universities(page, per_page, responses, option):
    """List all universities"""
    try:
        api_client = HTBAPIClient()
        universities_module = UniversitiesModule(api_client)
        result = universities_module.get_university_all_list(page, per_page)
        
        if result and 'data' in result:
            universities_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            if responses:
                # Show all available fields for first university
                if universities_data:
                    first_university = universities_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Universities[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_university.items()])}",
                        title=f"Universities - All Fields (First Item, Page {page})"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title=f"Universities - Selected Fields (Page {page})")
                table.add_column("ID", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for university in universities_data:
                    row = [str(university.get('id', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(university.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title=f"Universities (Page {page})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Country", style="yellow")
                table.add_column("Users", style="magenta")
                table.add_column("Respected", style="blue")
                table.add_column("Created", style="red")
                
                try:
                    for university in universities_data:
                        table.add_row(
                            str(university.get('id', 'N/A') or 'N/A'),
                            str(university.get('name', 'N/A') or 'N/A'),
                            str(university.get('country', 'N/A') or 'N/A'),
                            str(university.get('users_count', 'N/A') or 'N/A'),
                            str(university.get('respected_by_count', 'N/A') or 'N/A'),
                            str(university.get('created_at', 'N/A') or 'N/A')[:10]  # Show just the date part
                        )
                    
                    console.print(table)
                except Exception as e:
                    console.print(f"[yellow]Error processing universities data: {e}[/yellow]")
                    console.print(f"[yellow]Data type: {type(universities_data)}[/yellow]")
                    console.print(f"[yellow]Data: {universities_data}[/yellow]")
        else:
            console.print("[yellow]No universities found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@universities.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('university_id', type=int)
def profile(university_id, debug, json_output):
    """Get university profile"""
    try:
        api_client = HTBAPIClient()
        universities_module = UniversitiesModule(api_client)
        result = universities_module.get_university_profile(university_id)
        
        if result and 'data' in result:
            profile_data = result['data']
            console.print(Panel.fit(
                f"[bold green]University Profile[/bold green]\n"
                f"Name: {profile_data.get('name', 'N/A') or 'N/A'}\n"
                f"Country: {profile_data.get('country', 'N/A') or 'N/A'}\n"
                f"Users: {profile_data.get('users_count', 'N/A') or 'N/A'}\n"
                f"Respected: {profile_data.get('respected_by_count', 'N/A') or 'N/A'}\n"
                f"Created: {profile_data.get('created_at', 'N/A') or 'N/A'}",
                title=f"University ID: {university_id}"
            ))
        else:
            console.print("[yellow]University not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@universities.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
def rankings(page, per_page):
    """Get university rankings"""
    try:
        api_client = HTBAPIClient()
        universities_module = UniversitiesModule(api_client)
        result = universities_module.get_university_top_list(page, per_page)
        
        if result and 'data' in result:
            rankings_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"University Rankings (Page {page})")
            table.add_column("Rank", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Country", style="yellow")
            table.add_column("Points", style="magenta")
            table.add_column("Users", style="blue")
            
            try:
                for ranking in rankings_data:
                    table.add_row(
                        str(ranking.get('rank', 'N/A') or 'N/A'),
                        str(ranking.get('name', 'N/A') or 'N/A'),
                        str(ranking.get('country', 'N/A') or 'N/A'),
                        str(ranking.get('points', 'N/A') or 'N/A'),
                        str(ranking.get('users_count', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing rankings data: {e}[/yellow]")
        else:
            console.print("[yellow]No rankings found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@universities.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('university_id', type=int)
def stats(university_id, debug, json_output):
    """Get university statistics"""
    try:
        api_client = HTBAPIClient()
        universities_module = UniversitiesModule(api_client)
        result = universities_module.get_university_activity(university_id)
        
        if result and 'data' in result:
            stats_data = result['data']
            console.print(Panel.fit(
                f"[bold green]University Statistics[/bold green]\n"
                f"Activity Count: {stats_data.get('activity_count', 'N/A') or 'N/A'}\n"
                f"Last Activity: {stats_data.get('last_activity', 'N/A') or 'N/A'}",
                title=f"University ID: {university_id}"
            ))
        else:
            console.print("[yellow]No statistics found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@universities.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('university_id', type=int)
def members(university_id, debug, json_output):
    """Get university members"""
    try:
        api_client = HTBAPIClient()
        universities_module = UniversitiesModule(api_client)
        result = universities_module.get_university_members(university_id)
        
        if result and 'data' in result:
            members_data = result['data']
            
            table = Table(title=f"University Members (ID: {university_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Username", style="green")
            table.add_column("Rank", style="yellow")
            table.add_column("Points", style="magenta")
            
            for member in members_data:
                table.add_row(
                    str(member.get('id', 'N/A') or 'N/A'),
                    str(member.get('username', 'N/A') or 'N/A'),
                    str(member.get('rank', 'N/A') or 'N/A'),
                    str(member.get('points', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No members found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@universities.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
def new_list(page, per_page):
    """Get new universities list"""
    try:
        api_client = HTBAPIClient()
        universities_module = UniversitiesModule(api_client)
        result = universities_module.get_university_new_list(page, per_page)
        
        if result and 'data' in result:
            new_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"New Universities (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Country", style="yellow")
            table.add_column("Created", style="magenta")
            
            try:
                for university in new_data:
                    table.add_row(
                        str(university.get('id', 'N/A') or 'N/A'),
                        str(university.get('name', 'N/A') or 'N/A'),
                        str(university.get('country', 'N/A') or 'N/A'),
                        str(university.get('created_at', 'N/A') or 'N/A')[:10]
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing new universities data: {e}[/yellow]")
        else:
            console.print("[yellow]No new universities found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@universities.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('user_id', type=int)
def user_stats(user_id, debug, json_output):
    """Get university owns statistics for a user"""
    try:
        api_client = HTBAPIClient()
        universities_module = UniversitiesModule(api_client)
        result = universities_module.get_university_stats_owns(user_id)
        
        if result and 'data' in result:
            stats_data = result['data']
            console.print(Panel.fit(
                f"[bold green]User University Stats[/bold green]\n"
                f"User ID: {user_id}\n"
                f"Total Owns: {stats_data.get('total_owns', 'N/A') or 'N/A'}\n"
                f"Machine Owns: {stats_data.get('machine_owns', 'N/A') or 'N/A'}\n"
                f"Challenge Owns: {stats_data.get('challenge_owns', 'N/A') or 'N/A'}",
                title="University Stats"
            ))
        else:
            console.print("[yellow]No user stats found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
