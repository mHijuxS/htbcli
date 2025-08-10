"""
Home module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class HomeModule:
    """Module for handling home-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_home_banners(self) -> Dict[str, Any]:
        """Get home banners"""
        return self.api.get("/home/banners")
    
    def get_home_recommended(self) -> Dict[str, Any]:
        """Get home recommended content"""
        return self.api.get("/home/recommended")
    
    def get_home_user_progress(self) -> Dict[str, Any]:
        """Get home user progress"""
        return self.api.get("/home/user/progress")
    
    def get_home_user_todo(self) -> Dict[str, Any]:
        """Get home user todo"""
        return self.api.get("/home/user/todo")

# Click commands
@click.group()
def home():
    """Home-related commands"""
    pass

@home.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def banners(responses, option):
    """Get home banners"""
    try:
        api_client = HTBAPIClient()
        home_module = HomeModule(api_client)
        result = home_module.get_home_banners()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Home Banners Data[/bold green]\n"
                    f"{result}",
                    title="Home Banners"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Home Banners[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="Home Banners"))
            else:
                # Show default fields
                if 'data' in result:
                    banners_data = result['data']
                    console.print(Panel.fit(
                        f"[bold green]Home Banners[/bold green]\n"
                        f"Count: {len(banners_data) if isinstance(banners_data, list) else 'N/A'}",
                        title="Home Banners"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Home Banners[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title="Home Banners"
                    ))
        else:
            console.print("[yellow]No banners found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@home.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def recommended(responses, option):
    """Get home recommended content"""
    try:
        api_client = HTBAPIClient()
        home_module = HomeModule(api_client)
        result = home_module.get_home_recommended()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Home Recommended Data[/bold green]\n"
                    f"{result}",
                    title="Home Recommended"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]Home Recommended[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="Home Recommended"))
            else:
                # Show default fields
                if 'data' in result:
                    recommended_data = result['data']
                    console.print(Panel.fit(
                        f"[bold green]Home Recommended[/bold green]\n"
                        f"Count: {len(recommended_data) if isinstance(recommended_data, list) else 'N/A'}",
                        title="Home Recommended"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]Home Recommended[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title="Home Recommended"
                    ))
        else:
            console.print("[yellow]No recommended content found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@home.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def user_progress(responses, option):
    """Get home user progress"""
    try:
        api_client = HTBAPIClient()
        home_module = HomeModule(api_client)
        result = home_module.get_home_user_progress()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Progress Data[/bold green]\n"
                    f"{result}",
                    title="User Progress"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Progress[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="User Progress"))
            else:
                # Show default fields
                if 'data' in result:
                    progress_data = result['data']
                    console.print(Panel.fit(
                        f"[bold green]User Progress[/bold green]\n"
                        f"Data available: {len(progress_data) if isinstance(progress_data, dict) else 'N/A'}",
                        title="User Progress"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]User Progress[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title="User Progress"
                    ))
        else:
            console.print("[yellow]No user progress found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@home.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def user_todo(responses, option):
    """Get home user todo"""
    try:
        api_client = HTBAPIClient()
        home_module = HomeModule(api_client)
        result = home_module.get_home_user_todo()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Todo Data[/bold green]\n"
                    f"{result}",
                    title="User Todo"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Todo[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="User Todo"))
            else:
                # Show default fields
                if 'data' in result:
                    todo_data = result['data']
                    console.print(Panel.fit(
                        f"[bold green]User Todo[/bold green]\n"
                        f"Count: {len(todo_data) if isinstance(todo_data, list) else 'N/A'}",
                        title="User Todo"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]User Todo[/bold green]\n"
                        f"Status: {result.get('status', 'N/A') or 'N/A'}",
                        title="User Todo"
                    ))
        else:
            console.print("[yellow]No user todo found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
