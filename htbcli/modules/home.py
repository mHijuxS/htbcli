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
    """Module for handling home page banner-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_home_banner(self) -> Dict[str, Any]:
        """Get home banner"""
        return self.api.get("/home/banner")
    
    def get_home_banner_announcement(self) -> Dict[str, Any]:
        """Get home banner announcement"""
        return self.api.get("/home/banner/announcement")
    
    def get_home_banner_changelog(self) -> Dict[str, Any]:
        """Get home banner changelog"""
        return self.api.get("/home/banner/changelog")
    
    def get_home_banner_notice(self) -> Dict[str, Any]:
        """Get home banner notice"""
        return self.api.get("/home/banner/notice")

# Click commands
@click.group()
def home():
    """Home page banner-related commands"""
    pass

@home.command()
def banner():
    """Get home banner"""
    try:
        api_client = HTBAPIClient()
        home_module = HomeModule(api_client)
        result = home_module.get_home_banner()
        
        if result and 'data' in result:
            banner_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Home Banner[/bold green]\n"
                f"Title: {banner_data.get('title', 'N/A') or 'N/A'}\n"
                f"Message: {banner_data.get('message', 'N/A') or 'N/A'}\n"
                f"Type: {banner_data.get('type', 'N/A') or 'N/A'}\n"
                f"Active: {banner_data.get('active', 'N/A') or 'N/A'}",
                title="Home Banner"
            ))
        else:
            console.print("[yellow]No banner found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@home.command()
def announcement():
    """Get home banner announcement"""
    try:
        api_client = HTBAPIClient()
        home_module = HomeModule(api_client)
        result = home_module.get_home_banner_announcement()
        
        if result and 'data' in result:
            announcement_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Banner Announcement[/bold green]\n"
                f"Title: {announcement_data.get('title', 'N/A') or 'N/A'}\n"
                f"Message: {announcement_data.get('message', 'N/A') or 'N/A'}\n"
                f"Date: {announcement_data.get('date', 'N/A') or 'N/A'}",
                title="Banner Announcement"
            ))
        else:
            console.print("[yellow]No announcement found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@home.command()
def changelog():
    """Get home banner changelog"""
    try:
        api_client = HTBAPIClient()
        home_module = HomeModule(api_client)
        result = home_module.get_home_banner_changelog()
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            table = Table(title="Banner Changelog")
            table.add_column("Date", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Description", style="yellow")
            table.add_column("Version", style="magenta")
            
            for change in changelog_data:
                table.add_row(
                    str(change.get('date', 'N/A') or 'N/A'),
                    str(change.get('type', 'N/A') or 'N/A'),
                    str(change.get('description', 'N/A') or 'N/A'),
                    str(change.get('version', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No changelog found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@home.command()
def notice():
    """Get home banner notice"""
    try:
        api_client = HTBAPIClient()
        home_module = HomeModule(api_client)
        result = home_module.get_home_banner_notice()
        
        if result and 'data' in result:
            notice_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Banner Notice[/bold green]\n"
                f"Title: {notice_data.get('title', 'N/A') or 'N/A'}\n"
                f"Message: {notice_data.get('message', 'N/A') or 'N/A'}\n"
                f"Type: {notice_data.get('type', 'N/A') or 'N/A'}\n"
                f"Priority: {notice_data.get('priority', 'N/A') or 'N/A'}",
                title="Banner Notice"
            ))
        else:
            console.print("[yellow]No notice found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
