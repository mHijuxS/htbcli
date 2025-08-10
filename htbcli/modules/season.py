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
    """Module for handling Season-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_season_list(self) -> Dict[str, Any]:
        """Get list of seasons"""
        return self.api.get("/season/list")
    
    def get_season_end(self, season_id: int, user_id: int) -> Dict[str, Any]:
        """Get user score for a season"""
        return self.api.get(f"/season/end/{season_id}/{user_id}")
    
    def get_season_machine_active(self) -> Dict[str, Any]:
        """Get active machines for the current season"""
        return self.api.get("/season/machine/active")
    
    def get_season_machines(self) -> Dict[str, Any]:
        """Get season machines"""
        return self.api.get("/season/machines")
    
    def get_season_machines_completed(self, season_id: int) -> Dict[str, Any]:
        """Get completed machines for a specific season"""
        return self.api.get(f"/season/machines/completed/{season_id}")
    
    def get_season_rewards(self, season_id: int) -> Dict[str, Any]:
        """Get Season Rewards"""
        return self.api.get(f"/season/rewards/{season_id}")
    
    def get_season_user_followers(self, season_id: int) -> Dict[str, Any]:
        """Get top season users and top ranked followers for a user"""
        return self.api.get(f"/season/user/followers/{season_id}")
    
    def get_season_user_rank(self, season_id: int) -> Dict[str, Any]:
        """Get user's rank for the current season"""
        return self.api.get(f"/season/user/rank/{season_id}")
    
    def get_season_leaderboard(self, leaderboard: str, season: Optional[str] = None) -> Dict[str, Any]:
        """Get season leaderboard"""
        params = {}
        if season:
            params["season"] = season
        return self.api.get(f"/season/{leaderboard}/leaderboard", params=params)
    
    def get_season_leaderboard_top(self, leaderboard: str, season_id: int, period: Optional[str] = None) -> Dict[str, Any]:
        """Get season top leaderboard"""
        params = {}
        if period:
            params["period"] = period
        return self.api.get(f"/season/{leaderboard}/leaderboard/top/{season_id}", params=params)

# Click commands
@click.group()
def season():
    """Season-related commands"""
    pass

@season.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_seasons(responses, option):
    """List seasons"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_list()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Seasons Data[/bold green]\n"
                    f"{result}",
                    title="Seasons"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Seasons[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="Seasons"))
            else:
                # Show default fields
                if 'data' in result:
                    seasons_data = result['data']
                    try:
                        count = len(seasons_data)
                        console.print(Panel.fit(
                            f"[bold green]Seasons[/bold green]\n"
                            f"Count: {count}",
                            title="Seasons"
                        ))
                    except:
                        console.print(Panel.fit(
                            f"[bold green]Seasons[/bold green]\n"
                            f"Data available: Yes",
                            title="Seasons"
                        ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Seasons[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title="Seasons"
                    ))
        else:
            console.print("[yellow]No seasons found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('season_id', type=int)
@click.argument('user_id', type=int)
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def end(season_id, user_id, responses, option):
    """Get user score for a season"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_end(season_id, user_id)
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Season End Data[/bold green]\n"
                    f"{result}",
                    title=f"Season {season_id} End - User {user_id}"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Season End[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title=f"Season {season_id} End - User {user_id}"))
            else:
                # Show default fields
                if 'data' in result:
                    end_data = result['data']
                    console.print(Panel.fit(
                        f"[bold green]Season End[/bold green]\n"
                        f"Season ID: {season_id}\n"
                        f"User ID: {user_id}\n"
                        f"Score: {end_data.get('score', 'N/A') or 'N/A'}",
                        title=f"Season {season_id} End - User {user_id}"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Season End[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title=f"Season {season_id} End - User {user_id}"
                    ))
        else:
            console.print("[yellow]No season end data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def machine_active(responses, option):
    """Get active machines for the current season"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_machine_active()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Active Season Machines Data[/bold green]\n"
                    f"{result}",
                    title="Active Season Machines"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Active Season Machines[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="Active Season Machines"))
            else:
                # Show default fields
                if 'data' in result:
                    machines_data = result['data']
                    try:
                        count = len(machines_data)
                        console.print(Panel.fit(
                            f"[bold green]Active Season Machines[/bold green]\n"
                            f"Count: {count}",
                            title="Active Season Machines"
                        ))
                    except:
                        console.print(Panel.fit(
                            f"[bold green]Active Season Machines[/bold green]\n"
                            f"Data available: Yes",
                            title="Active Season Machines"
                        ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Active Season Machines[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title="Active Season Machines"
                    ))
        else:
            console.print("[yellow]No active season machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
@click.option('--count-only', is_flag=True, help='Show only the count of machines')
def machines(responses, option, count_only):
    """Get season machines"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_machines()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Season Machines Data[/bold green]\n"
                    f"{result}",
                    title="Season Machines"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Season Machines[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="Season Machines"))
            elif count_only:
                # Show only count
                if 'data' in result:
                    machines_data = result['data']
                    count = len(machines_data) if isinstance(machines_data, list) else 'N/A'
                    console.print(Panel.fit(
                        f"[bold green]Season Machines[/bold green]\n"
                        f"Count: {count}",
                        title="Season Machines"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Season Machines[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title="Season Machines"
                    ))
            else:
                # Show machines in table format
                if 'data' in result:
                    machines_data = result['data']
                    if isinstance(machines_data, list) and machines_data:
                        table = Table(title="Season Machines")
                        table.add_column("Name", style="green")
                        table.add_column("Difficulty", style="yellow")
                        table.add_column("Rooted", style="cyan")
                        table.add_column("OS", style="magenta")
                        table.add_column("Points", style="blue")
                        
                        for machine in machines_data:
                            name = str(machine.get('name', 'N/A') or 'N/A')
                            difficulty = str(machine.get('difficulty_text', 'N/A') or 'N/A')
                            is_owned_root = machine.get('is_owned_root', False)
                            rooted = "Yes" if is_owned_root else "No"
                            os = str(machine.get('os', 'N/A') or 'N/A')
                            points = str(machine.get('root_points', 'N/A') or 'N/A')
                            
                            table.add_row(name, difficulty, rooted, os, points)
                        
                        console.print(table)
                    else:
                        console.print("[yellow]No machines data available[/yellow]")
                else:
                    console.print(Panel.fit(
                        f"[bold green]Season Machines[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title="Season Machines"
                    ))
        else:
            console.print("[yellow]No season machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('season_id', type=int)
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def machines_completed(season_id, responses, option):
    """Get completed machines for a specific season"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_machines_completed(season_id)
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Completed Machines Data[/bold green]\n"
                    f"{result}",
                    title=f"Season {season_id} Completed Machines"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Completed Machines[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title=f"Season {season_id} Completed Machines"))
            else:
                # Show default fields
                if 'data' in result:
                    completed_data = result['data']
                    count = len(completed_data) if isinstance(completed_data, list) else 'N/A'
                    console.print(Panel.fit(
                        f"[bold green]Completed Machines[/bold green]\n"
                        f"Season ID: {season_id}\n"
                        f"Count: {count}",
                        title=f"Season {season_id} Completed Machines"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Completed Machines[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title=f"Season {season_id} Completed Machines"
                    ))
        else:
            console.print("[yellow]No completed machines found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('season_id', type=int)
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def rewards(season_id, responses, option):
    """Get Season Rewards"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_rewards(season_id)
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Season Rewards Data[/bold green]\n"
                    f"{result}",
                    title=f"Season {season_id} Rewards"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Season Rewards[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title=f"Season {season_id} Rewards"))
            else:
                # Show default fields
                if 'data' in result:
                    rewards_data = result['data']
                    count = len(rewards_data) if isinstance(rewards_data, list) else 'N/A'
                    console.print(Panel.fit(
                        f"[bold green]Season Rewards[/bold green]\n"
                        f"Season ID: {season_id}\n"
                        f"Count: {count}",
                        title=f"Season {season_id} Rewards"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Season Rewards[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title=f"Season {season_id} Rewards"
                    ))
        else:
            console.print("[yellow]No season rewards found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('season_id', type=int)
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def user_followers(season_id, responses, option):
    """Get top season users and top ranked followers for a user"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_user_followers(season_id)
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Followers Data[/bold green]\n"
                    f"{result}",
                    title=f"Season {season_id} User Followers"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Followers[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title=f"Season {season_id} User Followers"))
            else:
                # Show default fields
                if 'data' in result:
                    followers_data = result['data']
                    data_count = len(followers_data) if isinstance(followers_data, dict) else 'N/A'
                    console.print(Panel.fit(
                        f"[bold green]User Followers[/bold green]\n"
                        f"Season ID: {season_id}\n"
                        f"Data available: {data_count}",
                        title=f"Season {season_id} User Followers"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]User Followers[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title=f"Season {season_id} User Followers"
                    ))
        else:
            console.print("[yellow]No user followers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('season_id', type=int)
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def user_rank(season_id, responses, option):
    """Get user's rank for the current season"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_user_rank(season_id)
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Rank Data[/bold green]\n"
                    f"{result}",
                    title=f"Season {season_id} User Rank"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Rank[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title=f"Season {season_id} User Rank"))
            else:
                # Show default fields
                if 'data' in result:
                    rank_data = result['data']
                    console.print(Panel.fit(
                        f"[bold green]User Rank[/bold green]\n"
                        f"Season ID: {season_id}\n"
                        f"Rank: {rank_data.get('rank', 'N/A') or 'N/A'}",
                        title=f"Season {season_id} User Rank"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]User Rank[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title=f"Season {season_id} User Rank"
                    ))
        else:
            console.print("[yellow]No user rank found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('leaderboard')
@click.option('--season', help='Season parameter')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def leaderboard(leaderboard, season, responses, option):
    """Get season leaderboard"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_leaderboard(leaderboard, season)
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Leaderboard Data[/bold green]\n"
                    f"{result}",
                    title=f"Season {leaderboard} Leaderboard"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Leaderboard[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title=f"Season {leaderboard} Leaderboard"))
            else:
                # Show default fields
                if 'data' in result:
                    leaderboard_data = result['data']
                    count = len(leaderboard_data) if isinstance(leaderboard_data, list) else 'N/A'
                    console.print(Panel.fit(
                        f"[bold green]Leaderboard[/bold green]\n"
                        f"Leaderboard: {leaderboard}\n"
                        f"Season: {season or 'N/A'}\n"
                        f"Count: {count}",
                        title=f"Season {leaderboard} Leaderboard"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Leaderboard[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title=f"Season {leaderboard} Leaderboard"
                    ))
        else:
            console.print("[yellow]No leaderboard found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@season.command()
@click.argument('leaderboard')
@click.argument('season_id', type=int)
@click.option('--period', help='Period parameter')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def leaderboard_top(leaderboard, season_id, period, responses, option):
    """Get season top leaderboard"""
    try:
        api_client = HTBAPIClient()
        season_module = SeasonModule(api_client)
        result = season_module.get_season_leaderboard_top(leaderboard, season_id, period)
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Top Leaderboard Data[/bold green]\n"
                    f"{result}",
                    title=f"Season {leaderboard} Top Leaderboard"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Top Leaderboard[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title=f"Season {leaderboard} Top Leaderboard"))
            else:
                # Show default fields
                if 'data' in result:
                    top_data = result['data']
                    count = len(top_data) if isinstance(top_data, list) else 'N/A'
                    console.print(Panel.fit(
                        f"[bold green]Top Leaderboard[/bold green]\n"
                        f"Leaderboard: {leaderboard}\n"
                        f"Season ID: {season_id}\n"
                        f"Period: {period or 'N/A'}\n"
                        f"Count: {count}",
                        title=f"Season {leaderboard} Top Leaderboard"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Top Leaderboard[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title=f"Season {leaderboard} Top Leaderboard"
                    ))
        else:
            console.print("[yellow]No top leaderboard found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
