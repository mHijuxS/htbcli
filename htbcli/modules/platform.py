"""
Platform module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class PlatformModule:
    """Module for handling platform-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_announcements(self) -> Dict[str, Any]:
        """Get announcements"""
        return self.api.get("/announcements")
    
    def get_changelogs(self) -> Dict[str, Any]:
        """Get platform changelogs"""
        return self.api.get("/changelogs")
    
    def get_content_stats(self) -> Dict[str, Any]:
        """Get content statistics"""
        return self.api.get("/content/stats")
    
    def get_lab_list(self) -> Dict[str, Any]:
        """Get lab list (HTB servers)"""
        return self.api.get("/lab/list")
    
    def get_navigation_main(self) -> Dict[str, Any]:
        """Get platform navigation details"""
        return self.api.get("/navigation/main")
    
    def get_notices(self) -> Dict[str, Any]:
        """Get platform notices"""
        return self.api.get("/notices")
    
    def get_search_fetch(self, query: str, tags: Optional[str] = None) -> Dict[str, Any]:
        """Fetch search results"""
        params = {"query": query}
        if tags:
            params["tags"] = tags
        return self.api.get("/search/fetch", params=params)
    
    def get_sidebar_announcement(self) -> Dict[str, Any]:
        """Get sidebar announcement"""
        return self.api.get("/sidebar/announcement")
    
    def get_sidebar_changelog(self) -> Dict[str, Any]:
        """Get sidebar changelog"""
        return self.api.get("/sidebar/changelog")

# Click commands
@click.group()
def platform():
    """General platform-related commands"""
    pass

@platform.command()
def announcements():
    """Get announcements"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_announcements()
        
        if result and 'data' in result:
            announcements_data = result['data']
            
            table = Table(title="Announcements")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Date", style="yellow")
            table.add_column("Type", style="magenta")
            
            for announcement in announcements_data:
                table.add_row(
                    str(announcement.get('id', 'N/A') or 'N/A'),
                    str(announcement.get('title', 'N/A') or 'N/A'),
                    str(announcement.get('date', 'N/A') or 'N/A'),
                    str(announcement.get('type', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No announcements found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@platform.command()
def changelogs():
    """Get platform changelogs"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_changelogs()
        
        if result and 'data' in result:
            changelogs_data = result['data']
            
            table = Table(title="Platform Changelogs")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Date", style="yellow")
            table.add_column("Type", style="magenta")
            
            for changelog in changelogs_data:
                table.add_row(
                    str(changelog.get('id', 'N/A') or 'N/A'),
                    str(changelog.get('title', 'N/A') or 'N/A'),
                    str(changelog.get('date', 'N/A') or 'N/A'),
                    str(changelog.get('type', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No changelogs found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@platform.command()
def content_stats():
    """Get content statistics"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_content_stats()
        
        if result and 'data' in result:
            stats = result['data']
            console.print(Panel.fit(
                f"[bold green]Content Statistics[/bold green]\n"
                f"Machines: {stats.get('machines', 'N/A') or 'N/A'}\n"
                f"Challenges: {stats.get('challenges', 'N/A') or 'N/A'}\n"
                f"Users: {stats.get('users', 'N/A') or 'N/A'}\n"
                f"Teams: {stats.get('teams', 'N/A') or 'N/A'}",
                title="Content Stats"
            ))
        else:
            console.print("[yellow]No content stats found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@platform.command()
def lab_list():
    """Get lab list (HTB servers)"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_lab_list()
        
        if result and 'data' in result:
            labs_data = result['data']
            
            table = Table(title="HTB Labs/Servers")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Location", style="yellow")
            table.add_column("Status", style="magenta")
            
            for lab in labs_data:
                table.add_row(
                    str(lab.get('id', 'N/A') or 'N/A'),
                    str(lab.get('name', 'N/A') or 'N/A'),
                    str(lab.get('location', 'N/A') or 'N/A'),
                    str(lab.get('status', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No labs found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@platform.command()
def navigation():
    """Get platform navigation details"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_navigation_main()
        
        if result and 'data' in result:
            nav_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Platform Navigation[/bold green]\n"
                f"Version: {nav_data.get('version', 'N/A') or 'N/A'}\n"
                f"Status: {nav_data.get('status', 'N/A') or 'N/A'}",
                title="Navigation Info"
            ))
        else:
            console.print("[yellow]No navigation data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@platform.command()
def notices():
    """Get platform notices"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_notices()
        
        if result and 'data' in result:
            notices_data = result['data']
            
            table = Table(title="Platform Notices")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Date", style="yellow")
            table.add_column("Type", style="magenta")
            
            for notice in notices_data:
                table.add_row(
                    str(notice.get('id', 'N/A') or 'N/A'),
                    str(notice.get('title', 'N/A') or 'N/A'),
                    str(notice.get('date', 'N/A') or 'N/A'),
                    str(notice.get('type', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No notices found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@platform.command()
@click.argument('query')
@click.option('--tags', help='Search tags')
def search(query, tags):
    """Search platform content"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_search_fetch(query, tags)
        
        # The search API returns data directly without a 'data' wrapper
        if result:
            # Check if we have any results in any category
            total_results = 0
            if result.get('machines'):
                total_results += len(result['machines'])
            if result.get('challenges'):
                total_results += len(result['challenges'])
            if result.get('users'):
                total_results += len(result['users'])
            if result.get('teams'):
                total_results += len(result['teams'])
            if result.get('joboffers'):
                total_results += len(result['joboffers'])
            
            if total_results == 0:
                console.print("[yellow]No search results found[/yellow]")
                return
            
            # Display results by category
            if result.get('machines'):
                table = Table(title=f"Machines - Search Results for '{query}'")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Avatar", style="yellow")
                table.add_column("Tier", style="magenta")
                table.add_column("Starting Point", style="blue")
                
                for machine in result['machines']:
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
            
            if result.get('challenges'):
                table = Table(title=f"Challenges - Search Results for '{query}'")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Category ID", style="yellow")
                table.add_column("Description", style="magenta")
                
                for challenge in result['challenges']:
                    # Truncate description if too long
                    description = challenge.get('description', 'N/A') or 'N/A'
                    if len(description) > 50:
                        description = description[:47] + "..."
                    
                    table.add_row(
                        str(challenge.get('id', 'N/A') or 'N/A'),
                        str(challenge.get('value', 'N/A') or 'N/A'),
                        str(challenge.get('challenge_category_id', 'N/A') or 'N/A'),
                        description
                    )
                console.print(table)
            
            if result.get('users'):
                table = Table(title=f"Users - Search Results for '{query}'")
                table.add_column("ID", style="cyan")
                table.add_column("Username", style="green")
                table.add_column("Avatar", style="yellow")
                
                for user in result['users']:
                    avatar_status = "Yes" if user.get('avatar') else "No"
                    table.add_row(
                        str(user.get('id', 'N/A') or 'N/A'),
                        str(user.get('value', 'N/A') or 'N/A'),
                        avatar_status
                    )
                console.print(table)
            
            if result.get('teams'):
                table = Table(title=f"Teams - Search Results for '{query}'")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Avatar", style="yellow")
                
                for team in result['teams']:
                    avatar_status = "Yes" if team.get('avatar') else "No"
                    table.add_row(
                        str(team.get('id', 'N/A') or 'N/A'),
                        str(team.get('value', 'N/A') or 'N/A'),
                        avatar_status
                    )
                console.print(table)
            
            if result.get('joboffers'):
                table = Table(title=f"Job Offers - Search Results for '{query}'")
                table.add_column("ID", style="cyan")
                table.add_column("Title", style="green")
                table.add_column("Company", style="yellow")
                table.add_column("Location", style="magenta")
                
                for job in result['joboffers']:
                    table.add_row(
                        str(job.get('id', 'N/A') or 'N/A'),
                        str(job.get('title', 'N/A') or 'N/A'),
                        str(job.get('company', 'N/A') or 'N/A'),
                        str(job.get('location', 'N/A') or 'N/A')
                    )
                console.print(table)
        else:
            console.print("[yellow]No search results found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@platform.command()
def sidebar_announcement():
    """Get sidebar announcement"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_sidebar_announcement()
        
        if result and 'data' in result:
            announcement = result['data']
            console.print(Panel.fit(
                f"[bold green]Sidebar Announcement[/bold green]\n"
                f"Title: {announcement.get('title', 'N/A') or 'N/A'}\n"
                f"Message: {announcement.get('message', 'N/A') or 'N/A'}\n"
                f"Date: {announcement.get('date', 'N/A') or 'N/A'}",
                title="Sidebar Announcement"
            ))
        else:
            console.print("[yellow]No sidebar announcement found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@platform.command()
def sidebar_changelog():
    """Get sidebar changelog"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_sidebar_changelog()
        
        if result and 'data' in result:
            changelog = result['data']
            console.print(Panel.fit(
                f"[bold green]Sidebar Changelog[/bold green]\n"
                f"Title: {changelog.get('title', 'N/A') or 'N/A'}\n"
                f"Content: {changelog.get('content', 'N/A') or 'N/A'}\n"
                f"Date: {changelog.get('date', 'N/A') or 'N/A'}",
                title="Sidebar Changelog"
            ))
        else:
            console.print("[yellow]No sidebar changelog found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
