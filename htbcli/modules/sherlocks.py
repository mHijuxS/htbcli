"""
Sherlocks module for HTB CLI
"""

import click
from typing import Dict, Any, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

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
    
    def search_sherlock_by_name(self, sherlock_name: str, max_pages: int = 5) -> Optional[int]:
        """Search for a sherlock by name and return its ID"""
        try:
            # Search through multiple pages to find the sherlock
            for page in range(1, max_pages + 1):
                result = self.get_sherlocks_list(page=page, per_page=20)
                
                if not result or 'data' not in result:
                    continue
                
                sherlocks = result['data']
                if not sherlocks:
                    continue
                
                # Search through sherlocks on this page
                for sherlock in sherlocks:
                    name = sherlock.get('name', '').lower()
                    sherlock_id = sherlock.get('id')
                    
                    # Check for exact match first
                    if name == sherlock_name.lower():
                        return sherlock_id
                    
                    # Check for partial match (contains)
                    if sherlock_name.lower() in name:
                        return sherlock_id
                
                # If no more sherlocks on this page, stop searching
                if len(sherlocks) < 20:
                    break
            
            return None
            
        except Exception as e:
            console.print(f"[red]Error searching for sherlock '{sherlock_name}': {e}[/red]")
            return None
    
    def resolve_sherlock_id(self, sherlock_identifier: Union[int, str]) -> Optional[int]:
        """Resolve sherlock identifier to sherlock ID"""
        if isinstance(sherlock_identifier, int):
            return sherlock_identifier
        elif isinstance(sherlock_identifier, str):
            # Try to convert to int first (in case it's a string number)
            try:
                return int(sherlock_identifier)
            except ValueError:
                # Search for sherlock by name
                console.print(f"[blue]Searching for sherlock: {sherlock_identifier}[/blue]")
                sherlock_id = self.search_sherlock_by_name(sherlock_identifier)
                if sherlock_id:
                    console.print(f"[green]✓[/green] Found sherlock ID: {sherlock_id} for '{sherlock_identifier}'")
                    return sherlock_id
                else:
                    console.print(f"[red]Could not find sherlock with name: {sherlock_identifier}[/red]")
                    return None
        else:
            console.print(f"[red]Invalid sherlock identifier type: {type(sherlock_identifier)}[/red]")
            return None

# Click commands
@click.group()
def sherlocks():
    """Sherlock-related commands"""
    pass

@sherlocks.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
@click.option('--difficulty', multiple=True, type=click.Choice(['very-easy', 'easy', 'medium', 'hard', 'insane']), help='Filter by difficulty (can be used multiple times)')
@click.option('--state', multiple=True, type=click.Choice(['active', 'retired', 'unreleased']), help='Filter by state (can be used multiple times)')
@click.option('--category', multiple=True, type=int, help='Filter by category ID (can be used multiple times)')
@click.option('--status', type=click.Choice(['completed', 'incompleted']), help='Filter by completion status')
@click.option('--sort-by', type=click.Choice(['solves', 'category', 'rating', 'name']), help='Sort by field')
@click.option('--sort-type', type=click.Choice(['asc', 'desc']), default='asc', help='Sort order')
@click.option('--keyword', help='Search by keyword')
@click.option('--todo', is_flag=True, help='Show only todo items')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def list_sherlocks(page, per_page, difficulty, state, category, status, sort_by, sort_type, keyword, todo, responses, option):
    """List sherlocks with filtering and sorting options"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Build parameters for filtering
        params = {
            'page': page,
            'per_page': per_page
        }
        
        # Add filtering parameters
        if difficulty:
            params['difficulty[]'] = list(difficulty)
        if state:
            params['state'] = list(state)
        if category:
            params['category[]'] = list(category)
        if status:
            params['status'] = status
        if sort_by:
            params['sort_by'] = sort_by
        if sort_type:
            params['sort_type'] = sort_type
        if keyword:
            params['keyword'] = keyword
        if todo:
            params['todo'] = 1
        
        result = sherlocks_module.get_sherlocks_list(page, per_page, **params)
        
        if result and 'data' in result:
            sherlocks_data = result['data']
            
            # Build title with filter info
            title_parts = [f"Sherlocks (Page {page})"]
            if difficulty:
                title_parts.append(f"Difficulty: {', '.join(difficulty)}")
            if state:
                title_parts.append(f"State: {', '.join(state)}")
            if status:
                title_parts.append(f"Status: {status}")
            if sort_by:
                title_parts.append(f"Sorted by: {sort_by} ({sort_type})")
            
            table = Table(title=" | ".join(title_parts))
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
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def categories(debug, json_output):
    """Get sherlocks categories list"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        result = sherlocks_module.get_sherlocks_categories_list()
        
        if handle_debug_option(debug, result, "Debug: Sherlock Categories API Response", json_output):
            return
        
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
@click.argument('sherlock_identifier')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def info(sherlock_identifier, responses, option):
    """Get sherlock info by ID or name"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Resolve sherlock identifier to sherlock ID
        sherlock_id = sherlocks_module.resolve_sherlock_id(sherlock_identifier)
        if sherlock_id is None:
            console.print(f"[red]Could not resolve sherlock identifier: {sherlock_identifier}[/red]")
            return
        
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
@click.argument('sherlock_identifier')
@click.option('--link-only', '-l', is_flag=True, help='Show only the download link without downloading')
@click.option('--output', '-o', help='Output filename (default: sherlock_{id}.zip)')
def download(sherlock_identifier, link_only, output):
    """Download sherlock file or show download link"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Resolve sherlock identifier to sherlock ID
        sherlock_id = sherlocks_module.resolve_sherlock_id(sherlock_identifier)
        if sherlock_id is None:
            console.print(f"[red]Could not resolve sherlock identifier: {sherlock_identifier}[/red]")
            return
        
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
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('sherlock_identifier')
def play(sherlock_identifier, debug, json_output):
    """Start or continue playing a sherlock"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Resolve sherlock identifier to sherlock ID
        sherlock_id = sherlocks_module.resolve_sherlock_id(sherlock_identifier)
        if sherlock_id is None:
            console.print(f"[red]Could not resolve sherlock identifier: {sherlock_identifier}[/red]")
            return
        
        result = sherlocks_module.get_sherlock_play(sherlock_id)
        
        if handle_debug_option(debug, result, f"Debug: Sherlock Play API Response (ID: {sherlock_id}, json_output)"):
            return
        
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
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('sherlock_identifier')
def progress(sherlock_identifier, debug, json_output):
    """Get sherlock progress"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Resolve sherlock identifier to sherlock ID
        sherlock_id = sherlocks_module.resolve_sherlock_id(sherlock_identifier)
        if sherlock_id is None:
            console.print(f"[red]Could not resolve sherlock identifier: {sherlock_identifier}[/red]")
            return
        
        result = sherlocks_module.get_sherlock_progress(sherlock_id)
        
        if handle_debug_option(debug, result, f"Debug: Sherlock Progress API Response (ID: {sherlock_id}, json_output)"):
            return
        
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
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('sherlock_identifier')
def tasks(sherlock_identifier, debug, json_output):
    """Get sherlock tasks"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Resolve sherlock identifier to sherlock ID
        sherlock_id = sherlocks_module.resolve_sherlock_id(sherlock_identifier)
        if sherlock_id is None:
            console.print(f"[red]Could not resolve sherlock identifier: {sherlock_identifier}[/red]")
            return
        
        result = sherlocks_module.get_sherlock_tasks(sherlock_id)
        
        if handle_debug_option(debug, result, f"Debug: Sherlock Tasks API Response (ID: {sherlock_id}, json_output)"):
            return
        
        if result and 'data' in result:
            tasks_data = result['data']
            
            table = Table(title=f"Sherlock Tasks (ID: {sherlock_id})")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="green")
            table.add_column("Description", style="yellow")
            table.add_column("Type", style="magenta")
            table.add_column("Completed", style="blue")
            
            for task in tasks_data:
                # Extract type text from the type object
                task_type = task.get('type', {})
                if isinstance(task_type, dict):
                    type_text = task_type.get('text', 'N/A')
                else:
                    type_text = str(task_type) if task_type else 'N/A'
                
                table.add_row(
                    str(task.get('id', 'N/A') or 'N/A'),
                    str(task.get('title', 'N/A') or 'N/A'),
                    str(task.get('description', 'N/A') or 'N/A'),
                    str(type_text),
                    str(task.get('completed', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No tasks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@sherlocks.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('sherlock_identifier')
@click.argument('task_id', type=int)
@click.argument('flag')
def submit_flag(sherlock_identifier, task_id, flag, debug, json_output):
    """Submit flag for a specific sherlock task"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Resolve sherlock identifier to sherlock ID
        sherlock_id = sherlocks_module.resolve_sherlock_id(sherlock_identifier)
        if sherlock_id is None:
            console.print(f"[red]Could not resolve sherlock identifier: {sherlock_identifier}[/red]")
            return
        
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
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('sherlock_identifier')
def writeup(sherlock_identifier, debug, json_output):
    """Get sherlock writeup"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Resolve sherlock identifier to sherlock ID
        sherlock_id = sherlocks_module.resolve_sherlock_id(sherlock_identifier)
        if sherlock_id is None:
            console.print(f"[red]Could not resolve sherlock identifier: {sherlock_identifier}[/red]")
            return
        
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
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('sherlock_identifier')
def writeup_official(sherlock_identifier, debug, json_output):
    """Get official sherlock writeup"""
    try:
        api_client = HTBAPIClient()
        sherlocks_module = SherlocksModule(api_client)
        
        # Resolve sherlock identifier to sherlock ID
        sherlock_id = sherlocks_module.resolve_sherlock_id(sherlock_identifier)
        if sherlock_id is None:
            console.print(f"[red]Could not resolve sherlock identifier: {sherlock_identifier}[/red]")
            return
        
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
