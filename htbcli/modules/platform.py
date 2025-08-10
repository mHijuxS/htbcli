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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def announcements(responses, option):
    """Get announcements"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_announcements()
        
        if result and 'data' in result:
            announcements_data = result['data']
            
            if responses:
                # Show all available fields for first announcement
                if announcements_data:
                    first_announcement = announcements_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Announcements[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_announcement.items()])}",
                        title="Announcements - All Fields (First Item)"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title="Announcements - Selected Fields")
                table.add_column("ID", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for announcement in announcements_data:
                    row = [str(announcement.get('id', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(announcement.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def changelogs(responses, option):
    """Get platform changelogs"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_changelogs()
        
        if result and 'data' in result:
            changelogs_data = result['data']
            
            if responses:
                # Show all available fields for first changelog
                if changelogs_data:
                    first_changelog = changelogs_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Changelogs[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_changelog.items()])}",
                        title="Changelogs - All Fields (First Item)"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title="Changelogs - Selected Fields")
                table.add_column("ID", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for changelog in changelogs_data:
                    row = [str(changelog.get('id', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(changelog.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def content_stats(responses, option):
    """Get content statistics"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_content_stats()
        
        if result and ('data' in result or result):
            stats = result.get('data') or result
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for Content Stats[/bold green]\n"
                    f"{chr(10).join([f'{k}: {v}' for k, v in stats.items()])}",
                    title="Content Stats - All Fields"
                ))
            elif option:
                # Show only specified fields
                selected_stats = {}
                for field in option:
                    if field in stats:
                        selected_stats[field] = stats[field]
                    else:
                        console.print(f"[yellow]Field '{field}' not found in response[/yellow]")
                
                if selected_stats:
                    console.print(Panel.fit(
                        f"[bold green]Selected Fields[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in selected_stats.items()])}",
                        title="Content Stats - Selected Fields"
                    ))
            else:
                # Default view
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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def lab_list(responses, option):
    """Get lab list (HTB servers)"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_lab_list()
        
        if result and 'data' in result:
            labs_data = result['data']
            
            if responses:
                # Show all available fields for first lab
                if labs_data:
                    first_lab = labs_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Labs[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_lab.items()])}",
                        title="Labs - All Fields (First Item)"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title="Labs - Selected Fields")
                table.add_column("ID", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for lab in labs_data:
                    row = [str(lab.get('id', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(lab.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def navigation(responses, option):
    """Get platform navigation details"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_navigation_main()
        
        if result and 'data' in result:
            nav_data = result['data']
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for Navigation[/bold green]\n"
                    f"{chr(10).join([f'{k}: {v}' for k, v in nav_data.items()])}",
                    title="Navigation - All Fields"
                ))
            elif option:
                # Show only specified fields
                selected_nav = {}
                for field in option:
                    if field in nav_data:
                        selected_nav[field] = nav_data[field]
                    else:
                        console.print(f"[yellow]Field '{field}' not found in response[/yellow]")
                
                if selected_nav:
                    console.print(Panel.fit(
                        f"[bold green]Selected Fields[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in selected_nav.items()])}",
                        title="Navigation - Selected Fields"
                    ))
            else:
                # Default view
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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def notices(responses, option):
    """Get platform notices"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_notices()
        
        if result and 'data' in result:
            notices_data = result['data']
            
            if responses:
                # Show all available fields for first notice
                if notices_data:
                    first_notice = notices_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Notices[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_notice.items()])}",
                        title="Notices - All Fields (First Item)"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title="Notices - Selected Fields")
                table.add_column("ID", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for notice in notices_data:
                    row = [str(notice.get('id', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(notice.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def sidebar_announcement(responses, option):
    """Get sidebar announcement"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_sidebar_announcement()
        
        if result and 'data' in result:
            announcement = result['data']
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for Sidebar Announcement[/bold green]\n"
                    f"{chr(10).join([f'{k}: {v}' for k, v in announcement.items()])}",
                    title="Sidebar Announcement - All Fields"
                ))
            elif option:
                # Show only specified fields
                selected_announcement = {}
                for field in option:
                    if field in announcement:
                        selected_announcement[field] = announcement[field]
                    else:
                        console.print(f"[yellow]Field '{field}' not found in response[/yellow]")
                
                if selected_announcement:
                    console.print(Panel.fit(
                        f"[bold green]Selected Fields[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in selected_announcement.items()])}",
                        title="Sidebar Announcement - Selected Fields"
                    ))
            else:
                # Default view
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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def sidebar_changelog(responses, option):
    """Get sidebar changelog"""
    try:
        api_client = HTBAPIClient()
        platform_module = PlatformModule(api_client)
        result = platform_module.get_sidebar_changelog()
        
        if result and 'data' in result:
            changelog = result['data']
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for Sidebar Changelog[/bold green]\n"
                    f"{chr(10).join([f'{k}: {v}' for k, v in changelog.items()])}",
                    title="Sidebar Changelog - All Fields"
                ))
            elif option:
                # Show only specified fields
                selected_changelog = {}
                for field in option:
                    if field in changelog:
                        selected_changelog[field] = changelog[field]
                    else:
                        console.print(f"[yellow]Field '{field}' not found in response[/yellow]")
                
                if selected_changelog:
                    console.print(Panel.fit(
                        f"[bold green]Selected Fields[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in selected_changelog.items()])}",
                        title="Sidebar Changelog - Selected Fields"
                    ))
            else:
                # Default view
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
