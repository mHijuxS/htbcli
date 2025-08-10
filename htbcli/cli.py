"""
Main CLI entry point for HTB CLI
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from . import __version__
from .config import Config
from .swagger_parser import SwaggerParser
from .modules import (
    machines, challenges, user, season, sherlocks,
    badges, career, connection, fortresses, home,
    platform, prolabs, pwnbox, ranking, review,
    starting_point, team, tracks, universities, vm, vpn
)

console = Console()

@click.group()
@click.version_option(version=__version__, prog_name="HTB CLI")
def cli():
    """
    HTB CLI - A command-line interface for HackTheBox API
    
    This CLI provides easy access to all HTB API endpoints organized by modules.
    Make sure to set your HTB_TOKEN environment variable before using.
    """
    pass

# Add all module commands
cli.add_command(machines)
cli.add_command(challenges)
cli.add_command(user)
cli.add_command(season)
cli.add_command(sherlocks)
cli.add_command(badges)
cli.add_command(career)
cli.add_command(connection)
cli.add_command(fortresses)
cli.add_command(home)
cli.add_command(platform)
cli.add_command(prolabs)
cli.add_command(pwnbox)
cli.add_command(ranking)
cli.add_command(review)
cli.add_command(starting_point)
cli.add_command(team)
cli.add_command(tracks)
cli.add_command(universities)
cli.add_command(vm)
cli.add_command(vpn)

@cli.command()
def info():
    """Show HTB CLI information and configuration"""
    try:
        console.print(Panel.fit(
            "[bold green]HTB CLI Information[/bold green]\n"
            f"API v4 Base URL: {Config.BASE_URL_V4}\n"
            f"API v5 Base URL: {Config.BASE_URL_V5}\n"
            f"API Token: {'[green]Set[/green]' if Config.API_TOKEN else '[red]Not Set[/red]'}\n"
            f"Default Per Page: {Config.DEFAULT_PER_PAGE}\n"
            f"Max Per Page: {Config.MAX_PER_PAGE}",
            title="Configuration"
        ))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
def endpoints():
    """List all available API endpoints from swagger file"""
    try:
        parser = SwaggerParser()
        tags = parser.get_tags()
        
        table = Table(title="Available API Modules")
        table.add_column("Module", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Endpoints", style="yellow")
        
        for tag in tags:
            endpoints = parser.get_endpoints_by_tag(tag['name'])
            table.add_row(
                tag['name'],
                tag.get('description', 'No description'),
                str(len(endpoints))
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
@click.argument('module_name')
def module_info(module_name):
    """Show detailed information about a specific module"""
    try:
        parser = SwaggerParser()
        endpoints = parser.get_endpoints_by_tag(module_name)
        
        if not endpoints:
            console.print(f"[yellow]Module '{module_name}' not found[/yellow]")
            return
        
        table = Table(title=f"Endpoints for {module_name}")
        table.add_column("Method", style="cyan")
        table.add_column("Path", style="green")
        table.add_column("Summary", style="yellow")
        table.add_column("Description", style="magenta")
        
        for endpoint in endpoints:
            table.add_row(
                endpoint['method'],
                endpoint['path'],
                endpoint['summary'],
                endpoint['description'][:50] + "..." if len(endpoint['description']) > 50 else endpoint['description']
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
def setup():
    """Setup HTB CLI configuration"""
    try:
        Config.ensure_config_dir()
        console.print(Panel.fit(
            "[bold green]HTB CLI Setup[/bold green]\n"
            "1. Get your API token from https://app.hackthebox.com\n"
            "2. Set the environment variable: export HTB_TOKEN='your_token_here'\n"
            "3. Or create a .env file with: HTB_TOKEN=your_token_here\n"
            "4. Run 'htbcli info' to verify your configuration",
            title="Setup Instructions"
        ))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == '__main__':
    cli()
