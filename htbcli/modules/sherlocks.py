"""
Sherlocks module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class SherlocksModule:
    """Module for handling Sherlock-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_sherlocks_list(self, page: int = 1, per_page: int = 20, **kwargs) -> Dict[str, Any]:
        """Get list of sherlocks"""
        params = {
            "page": page,
            "per_page": per_page
        }
        # Add optional parameters
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        return self.api.get("/sherlocks", params=params)
    
    def get_sherlocks_categories_list(self) -> Dict[str, Any]:
        """Get sherlocks categories list"""
        return self.api.get("/sherlocks/categories/list")
    
    def get_sherlock_info(self, sherlock_id: int) -> Dict[str, Any]:
        """Get sherlock info by ID"""
        return self.api.get(f"/sherlocks/{sherlock_id}/info")
    
    def get_sherlock_download_link(self, sherlock_id: int) -> Dict[str, Any]:
        """Get sherlock download link"""
        return self.api.get(f"/sherlocks/{sherlock_id}/download_link")
    
    def get_sherlock_play(self, sherlock_id: int) -> Dict[str, Any]:
        """Start or continue playing a sherlock"""
        return self.api.get(f"/sherlocks/{sherlock_id}/play")
    
    def get_sherlock_progress(self, sherlock_id: int) -> Dict[str, Any]:
        """Get sherlock progress"""
        return self.api.get(f"/sherlocks/{sherlock_id}/progress")
    
    def get_sherlock_tasks(self, sherlock_id: int) -> Dict[str, Any]:
        """Get sherlock tasks"""
        return self.api.get(f"/sherlocks/{sherlock_id}/tasks")
    
    def submit_sherlock_task_flag(self, sherlock_id: int, task_id: int, flag: str) -> Dict[str, Any]:
        """Submit flag for a specific sherlock task"""
        return self.api.post(f"/sherlocks/{sherlock_id}/tasks/{task_id}/flag", json_data={"flag": flag})
    
    def get_sherlock_writeup(self, sherlock_id: int) -> Dict[str, Any]:
        """Get sherlock writeup"""
        return self.api.get(f"/sherlocks/{sherlock_id}/writeup")
    
    def get_sherlock_writeup_official(self, sherlock_id: int) -> Dict[str, Any]:
        """Get official sherlock writeup"""
        return self.api.get(f"/sherlocks/{sherlock_id}/writeup/official")

# Click commands
@click.group()
def sherlocks():
    """Sherlock-related commands"""
    pass

@sherlocks.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_sherlocks(page, per_page, responses, option):
    """List sherlocks"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlocks_list(page, per_page)
        
        if result and 'data' in result:
            sherlocks_data = result['data']
            
            table = Table(title=f"Sherlocks (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Category", style="yellow")
            table.add_column("Difficulty", style="magenta")
            table.add_column("State", style="blue")
            table.add_column("Solves", style="red")
            
            try:
                for sherlock in sherlocks_data:
                    table.add_row(
                        str(sherlock.get('id', 'N/A') or 'N/A'),
                        str(sherlock.get('name', 'N/A') or 'N/A'),
                        str(sherlock.get('category_name', 'N/A') or 'N/A'),
                        str(sherlock.get('difficulty', 'N/A') or 'N/A'),
                        str(sherlock.get('state', 'N/A') or 'N/A'),
                        str(sherlock.get('solves', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            except Exception as e:
                console.print(f"[yellow]Error processing sherlocks data: {e}[/yellow]")
        else:
            console.print("[yellow]No sherlocks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
def categories():
    """Get sherlocks categories list"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlocks_categories_list()
        
        if result and 'info' in result:
            categories_data = result['info']
            
            table = Table(title="Sherlock Categories")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Description", style="yellow")
            
            for category in categories_data:
                table.add_row(
                    str(category.get('id', 'N/A') or 'N/A'),
                    str(category.get('name', 'N/A') or 'N/A'),
                    str(category.get('description', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No categories found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def info(sherlock_id, responses, option):
    """Get sherlock info by ID"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_info(sherlock_id)
        
        if result and 'data' in result:
            info = result['data']
            
            if responses:
                console.print(Panel.fit(str(result), title="Full Response"))
            elif option:
                for opt in option:
                    if opt in info:
                        console.print(f"{opt}: {info[opt]}")
                    else:
                        console.print(f"[yellow]Field '{opt}' not found[/yellow]")
            else:
                console.print(Panel.fit(
                    f"[bold green]Sherlock Info[/bold green]\n"
                    f"ID: {info.get('id', 'N/A') or 'N/A'}\n"
                    f"Description: {info.get('description', 'N/A') or 'N/A'}\n"
                    f"User Owns: {info.get('user_owns_count', 'N/A') or 'N/A'}\n"
                    f"Academy Modules: {len(info.get('academyModules', []))}",
                    title=f"Sherlock ID: {sherlock_id}"
                ))
        else:
            console.print("[yellow]Sherlock not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
@click.option('--link-only', '-l', is_flag=True, help='Show only the download link without downloading')
@click.option('--output', '-o', help='Output filename (default: sherlock_{id}.zip)')
def download(sherlock_id, link_only, output):
    """Download sherlock file or show download link"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_download_link(sherlock_id)
        
        if result and 'url' in result:
            download_url = result.get('url')
            expires_in = result.get('expires_in', 'N/A')
            
            if link_only:
                # Just show the link
                console.print(Panel.fit(
                    f"[bold green]Download Link[/bold green]\n"
                    f"URL: {download_url}\n"
                    f"Expires In: {expires_in} seconds\n\n"
                    f"[blue]Use without --link-only flag to download the file directly[/blue]",
                    title=f"Sherlock ID: {sherlock_id}"
                ))
            else:
                # Download the file
                import requests
                import os
                
                # Determine output filename
                if output:
                    filename = output
                else:
                    filename = f"sherlock_{sherlock_id}.zip"
                
                console.print(f"[blue]Downloading sherlock {sherlock_id} to {filename}...[/blue]")
                
                try:
                    # Use the API client's session to maintain authentication
                    response = api_client.session.get(download_url, allow_redirects=True, stream=True)
                    response.raise_for_status()
                    
                    # Get content length for progress
                    total_size = int(response.headers.get('content-length', 0))
                    
                    with open(filename, 'wb') as f:
                        downloaded = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                if total_size > 0:
                                    percent = (downloaded / total_size) * 100
                                    console.print(f"\r[blue]Downloading... {percent:.1f}% ({downloaded}/{total_size} bytes)[/blue]", end="")
                    
                    console.print(f"\n[green]✓[/green] Successfully downloaded to {filename}")
                    
                except Exception as download_error:
                    console.print(f"[red]Download failed: {download_error}[/red]")
                    # Fall back to showing the link
                    console.print(Panel.fit(
                        f"[bold green]Download Link[/bold green]\n"
                        f"URL: {download_url}\n"
                        f"Expires In: {expires_in} seconds\n\n"
                        f"[yellow]Download failed, but you can manually download from the URL above[/yellow]",
                        title=f"Sherlock ID: {sherlock_id}"
                    ))
        else:
            console.print("[yellow]Download link not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def play(sherlock_id):
    """Start or continue playing a sherlock"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_play(sherlock_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Play Result[/bold green]\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title=f"Sherlock ID: {sherlock_id}"
            ))
        else:
            console.print("[yellow]No play result[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def progress(sherlock_id):
    """Get sherlock progress"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_progress(sherlock_id)
        
        if result and 'data' in result:
            progress_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Progress[/bold green]\n"
                f"Tasks Answered: {progress_data.get('tasks_answered', 'N/A') or 'N/A'}\n"
                f"Total Tasks: {progress_data.get('total_tasks', 'N/A') or 'N/A'}\n"
                f"Progress: {progress_data.get('progress', 'N/A') or 'N/A'}%\n"
                f"Own Rank: {progress_data.get('own_rank', 'N/A') or 'N/A'}\n"
                f"Is Owned: {progress_data.get('is_owned', 'N/A') or 'N/A'}",
                title=f"Sherlock ID: {sherlock_id}"
            ))
        else:
            console.print("[yellow]No progress data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def tasks(sherlock_id):
    """Get sherlock tasks"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_tasks(sherlock_id)
        
        if result and 'data' in result:
            tasks_data = result['data']
            
            table = Table(title=f"Sherlock Tasks (ID: {sherlock_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Description", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Completed", style="blue")
            
            for task in tasks_data:
                table.add_row(
                    str(task.get('id', 'N/A') or 'N/A'),
                    str(task.get('title', 'N/A') or 'N/A'),
                    str(task.get('description', 'N/A') or 'N/A'),
                    str(task.get('type', 'N/A') or 'N/A'),
                    str(task.get('completed', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No tasks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
@click.argument('task_id', type=int)
@click.argument('flag')
def submit_flag(sherlock_id, task_id, flag):
    """Submit flag for a specific sherlock task"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.submit_sherlock_task_flag(sherlock_id, task_id, flag)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Flag Submission Result[/bold green]\n"
                f"Sherlock ID: {sherlock_id}\n"
                f"Task ID: {task_id}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Flag Submission"
            ))
        else:
            console.print("[yellow]No result from flag submission[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def writeup(sherlock_id):
    """Get sherlock writeup"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_writeup(sherlock_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Writeup[/bold green]\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title=f"Sherlock ID: {sherlock_id}"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.argument('sherlock_id', type=int)
def writeup_official(sherlock_id):
    """Get official sherlock writeup"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlock_writeup_official(sherlock_id)
        
        if result and 'data' in result:
            writeup_data = result['data']
            console.print(Panel.fit(
                f"[bold green]Official Writeup[/bold green]\n"
                f"Title: {writeup_data.get('title', 'N/A') or 'N/A'}\n"
                f"Author: {writeup_data.get('author', 'N/A') or 'N/A'}\n"
                f"Content: {writeup_data.get('content', 'N/A') or 'N/A'}",
                title=f"Sherlock ID: {sherlock_id}"
            ))
        else:
            console.print("[yellow]No official writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
