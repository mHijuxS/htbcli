"""
Challenges module for HTB CLI
"""

import click
import sys
from typing import Dict, Any, Optional, Union, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

class ChallengesModule:
    """Module for handling challenge-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_challenge_activity(self, challenge_id: int) -> Dict[str, Any]:
        """Get challenge activity"""
        return self.api.get(f"/challenge/activity/{challenge_id}")
    
    def get_challenge_categories_list(self) -> Dict[str, Any]:
        """Get challenge categories list"""
        return self.api.get("/challenge/categories/list")
    
    def get_challenge_changelog(self, challenge_id: int) -> Dict[str, Any]:
        """Get challenge changelog"""
        return self.api.get(f"/challenge/changelog/{challenge_id}")
    
    def get_challenge_download(self, challenge_id: int) -> bytes:
        """Download challenge files"""
        return self.api.get_binary(f"/challenge/download/{challenge_id}")
    
    def get_challenge_info(self, challenge_slug: str) -> Dict[str, Any]:
        """Get challenge info by slug"""
        return self.api.get(f"/challenge/info/{challenge_slug}")
    
    def get_challenge_info_by_id(self, challenge_id: int) -> Dict[str, Any]:
        """Get challenge info by ID by searching through challenges list to find the slug, then get detailed info"""
        try:
            # First, search through challenges list to find the challenge slug
            for page in range(1, 6):  # Search first 5 pages
                result = self.get_challenges(page=page, per_page=20)
                
                if not result or 'data' not in result:
                    continue
                
                challenges = result['data']
                if not challenges:
                    continue
                
                # Search through challenges on this page
                for challenge in challenges:
                    if challenge.get('id') == challenge_id:
                        # Found the challenge, now get detailed info using the slug
                        # Try to get slug from different possible fields
                        slug = challenge.get('url_name') or challenge.get('slug')
                        
                        # If no slug field, generate one from the name
                        if not slug and challenge.get('name'):
                            slug = challenge.get('name').lower().replace(' ', '-').replace('_', '-')
                        
                        if slug:
                            try:
                                # Use the actual challenge info API endpoint
                                detailed_info = self.get_challenge_info(slug)
                                return detailed_info
                            except Exception:
                                # If API call fails, fallback to challenges list data
                                return {'data': challenge}
                        else:
                            # Fallback to challenges list data
                            return {'data': challenge}
            
            return None
        except Exception:
            return None
    
    def get_active_challenges(self) -> List[Dict[str, Any]]:
        """Get list of active challenge instances"""
        active_challenges = []
        
        try:
            # Search through challenges to find active instances
            for page in range(1, 3):  # Limit to first 2 pages to avoid rate limits
                result = self.get_challenges(page=page, per_page=20)
                
                if not result or 'data' not in result:
                    continue
                
                challenges = result['data']
                if not challenges:
                    continue
                
                # Check each challenge for active instances
                for challenge in challenges:
                    challenge_id = challenge.get('id')
                    if challenge_id:
                        try:
                            # Get detailed challenge info to check for active instances
                            challenge_info = self.get_challenge_info_by_id(challenge_id)
                            if challenge_info and 'challenge' in challenge_info:
                                challenge_data = challenge_info['challenge']
                                
                                # Check if challenge has an active instance
                                if challenge_data.get('docker_status') == 'ready' and challenge_data.get('docker_ip'):
                                    active_challenges.append({
                                        'id': challenge_id,
                                        'name': challenge_data.get('name', 'N/A'),
                                        'difficulty': challenge_data.get('difficulty', 'N/A'),
                                        'category': challenge_data.get('category_name', 'N/A'),
                                        'ip': challenge_data.get('docker_ip', 'N/A'),
                                        'ports': challenge_data.get('docker_ports', []),
                                        'status': challenge_data.get('docker_status', 'N/A')
                                    })
                        except Exception:
                            # Skip challenges that can't be checked
                            continue
                            
                        # Limit to avoid rate limits - only check first few challenges
                        if len(active_challenges) >= 5:
                            break
                    
                    # Limit to avoid rate limits
                    if len(active_challenges) >= 5:
                        break
                        
        except Exception as e:
            console.print(f"[yellow]Warning: Could not check all challenges due to rate limits: {e}[/yellow]")
        
        return active_challenges
    
    def submit_challenge_flag(self, flag: str, challenge_id: int, difficulty: int) -> Dict[str, Any]:
        """Submit flag for challenge"""
        return self.api.post("/challenge/own", json_data={"flag": flag, "challenge_id": challenge_id, "difficulty": difficulty})
    
    def get_challenge_recommended(self) -> Dict[str, Any]:
        """Get recommended challenges"""
        return self.api.get("/challenge/recommended")
    
    def get_challenge_recommended_retired(self) -> Dict[str, Any]:
        """Get recommended retired challenges"""
        return self.api.get("/challenge/recommended/retired")
    
    def submit_challenge_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit challenge review"""
        return self.api.post("/challenge/review", json_data=review_data)
    
    def mark_review_helpful(self, review_id: int) -> Dict[str, Any]:
        """Mark review as helpful"""
        return self.api.post(f"/challenge/review/helpful/{review_id}")
    
    def get_challenge_reviews_user(self, challenge_id: int) -> Dict[str, Any]:
        """Get user's review for challenge"""
        return self.api.get(f"/challenge/reviews/user/{challenge_id}")
    
    def start_challenge(self, challenge_id: int) -> Dict[str, Any]:
        """Start a challenge"""
        return self.api.post("/challenge/start", json_data={"challenge_id": challenge_id})
    
    def stop_challenge(self, challenge_id: int) -> Dict[str, Any]:
        """Stop a challenge"""
        return self.api.post("/challenge/stop", json_data={"challenge_id": challenge_id})
    
    def get_challenge_suggested(self) -> Dict[str, Any]:
        """Get suggested challenges"""
        return self.api.get("/challenge/suggested")
    
    def get_challenge_writeup(self, challenge_id: int) -> Dict[str, Any]:
        """Get challenge writeup"""
        return self.api.get(f"/challenge/{challenge_id}/writeup")
    
    def get_challenge_writeup_official(self, challenge_id: int) -> bytes:
        """Get official challenge writeup"""
        return self.api.get_binary(f"/challenge/{challenge_id}/writeup/official")
    
    def get_challenges(
        self, 
        page: int = 1, 
        per_page: int = 20,
        status: Optional[str] = None,
        state: Optional[list] = None,
        sort_by: Optional[str] = None,
        sort_type: Optional[str] = None,
        difficulty: Optional[list] = None,
        category: Optional[list] = None,
        todo: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get list of challenges with filtering options"""
        params = {
            "page": page,
            "per_page": per_page
        }
        
        if status:
            params["status"] = status
        if state:
            params["state"] = state
        if sort_by:
            params["sort_by"] = sort_by
        if sort_type:
            params["sort_type"] = sort_type
        if difficulty:
            params["difficulty[]"] = difficulty
        if category:
            params["category[]"] = category
        if todo:
            params["todo"] = todo
            
        return self.api.get("/challenges", params=params)
    
    def search_challenge_by_name(self, challenge_name: str, max_pages: int = 5) -> Optional[int]:
        """Search for a challenge by name and return its ID"""
        try:
            # Search through multiple pages to find the challenge
            for page in range(1, max_pages + 1):
                result = self.get_challenges(page=page, per_page=20)
                
                if not result or 'data' not in result:
                    continue
                
                challenges = result['data']
                if not challenges:
                    continue
                
                # Search through challenges on this page
                for challenge in challenges:
                    name = challenge.get('name', '').lower()
                    challenge_id = challenge.get('id')
                    
                    # Check for exact match first
                    if name == challenge_name.lower():
                        return challenge_id
                    
                    # Check for partial match (contains)
                    if challenge_name.lower() in name:
                        return challenge_id
                
                # If no more challenges on this page, stop searching
                if len(challenges) < 20:
                    break
            
            return None
            
        except Exception as e:
            console.print(f"[red]Error searching for challenge '{challenge_name}': {e}[/red]")
            return None
    
    def resolve_challenge_id(self, challenge_identifier: Union[int, str]) -> Optional[int]:
        """Resolve challenge identifier to challenge ID"""
        if isinstance(challenge_identifier, int):
            return challenge_identifier
        elif isinstance(challenge_identifier, str):
            # Try to convert to int first (in case it's a string number)
            try:
                return int(challenge_identifier)
            except ValueError:
                # Search for challenge by name
                console.print(f"[blue]Searching for challenge: {challenge_identifier}[/blue]")
                challenge_id = self.search_challenge_by_name(challenge_identifier)
                if challenge_id:
                    console.print(f"[green]✓[/green] Found challenge ID: {challenge_id} for '{challenge_identifier}'")
                    return challenge_id
                else:
                    console.print(f"[red]Could not find challenge with name: {challenge_identifier}[/red]")
                    return None
        else:
            console.print(f"[red]Invalid challenge identifier type: {type(challenge_identifier)}[/red]")
            return None
    
    def resolve_category_id(self, category_identifier: Union[int, str]) -> Optional[int]:
        """Resolve category identifier to category ID"""
        if isinstance(category_identifier, int):
            return category_identifier
        elif isinstance(category_identifier, str):
            # Try to convert to int first (in case it's a string number)
            try:
                return int(category_identifier)
            except ValueError:
                # Search for category by name
                console.print(f"[blue]Searching for category: {category_identifier}[/blue]")
                category_id = self.search_category_by_name(category_identifier)
                if category_id:
                    console.print(f"[green]✓[/green] Found category ID: {category_id} for '{category_identifier}'")
                    return category_id
                else:
                    console.print(f"[red]Could not find category with name: {category_identifier}[/red]")
                    return None
        else:
            console.print(f"[red]Invalid category identifier type: {type(category_identifier)}[/red]")
            return None
    
    def search_category_by_name(self, category_name: str) -> Optional[int]:
        """Search for a category by name and return its ID"""
        try:
            result = self.get_challenge_categories_list()
            
            if not result or ('data' not in result and 'info' not in result):
                console.print(f"[yellow]No data in categories response[/yellow]")
                return None
            
            categories = result.get('data') or result.get('info')
            if not categories:
                console.print(f"[yellow]No categories found[/yellow]")
                return None
            
            # Search through categories with improved matching logic
            exact_matches = []
            partial_matches = []
            
            for category in categories:
                name = category.get('name', '').lower()
                category_id = category.get('id')
                search_term = category_name.lower()
                
                # Check for exact match first
                if name == search_term:
                    exact_matches.append((category_id, name))
                
                # Check for word boundary matches (more precise than simple contains)
                elif search_term in name:
                    # Check if it's a word boundary match (not just substring)
                    # This prevents "pwn" from matching "GamePwn"
                    words = name.split()
                    for word in words:
                        if (search_term == word or 
                            search_term in word.split('-') or 
                            search_term in word.split('_')):
                            partial_matches.append((category_id, name))
                            break
            
            # Return exact match if found
            if exact_matches:
                return exact_matches[0][0]
            
            # Return first partial match if found
            if partial_matches:
                return partial_matches[0][0]
            
            return None
            
        except Exception as e:
            console.print(f"[red]Error searching for category '{category_name}': {e}[/red]")
            return None
    
    def update_todo(self, product: str, product_id: int, todo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update todo list"""
        return self.api.post(f"/{product}/todo/update/{product_id}", json_data=todo_data)

# Click commands
@click.group()
def challenges():
    """Challenge-related commands"""
    pass

@challenges.command()
@click.option('--page', default=1, help='Page number')
@click.option('--per-page', default=20, help='Results per page')
@click.option('--status', 
              type=click.Choice(['incompleted', 'complete']),
              help='Filter by completion status')
@click.option('--state', 
              multiple=True,
              type=click.Choice(['active', 'retired', 'unreleased']),
              help='Filter by state (can be used multiple times)')
@click.option('--sort-by', 
              type=click.Choice(['release-date', 'name', 'user-owns', 'system-owns', 'rating', 'user-difficulty']),
              help='Sort by field')
@click.option('--sort-type', 
              type=click.Choice(['asc', 'desc']),
              help='Sort type (asc or desc)')
@click.option('--difficulty', 
              multiple=True,
              type=click.Choice(['very-easy', 'easy', 'medium', 'hard', 'insane']),
              help='Filter by difficulty (can be used multiple times)')
@click.option('--category', 
              multiple=True,
              help='Filter by category ID or name (can be used multiple times)')
@click.option('--todo', 
              is_flag=True,
              help='Show only challenges in todo list')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def list_challenges(page, per_page, status, state, sort_by, sort_type, difficulty, category, todo, responses, option, debug, json_output):
    """List challenges with filtering options"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Convert difficulty and state from tuples to lists if they exist
        difficulty_list = list(difficulty) if difficulty else None
        state_list = list(state) if state else None
        
        # Resolve category identifiers to IDs
        category_list = None
        if category:
            resolved_categories = []
            for cat in category:
                category_id = challenges_module.resolve_category_id(cat)
                if category_id is not None:
                    resolved_categories.append(category_id)
                else:
                    # If any category fails to resolve, skip the entire request
                    return
            category_list = resolved_categories if resolved_categories else None
        
        # Convert todo flag to integer if set
        todo_value = 1 if todo else None
        
        result = challenges_module.get_challenges(
            page=page, 
            per_page=per_page,
            status=status,
            state=state_list,
            sort_by=sort_by,
            sort_type=sort_type,
            difficulty=difficulty_list,
            category=category_list,
            todo=todo_value
        )
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Challenges List", json_output)
            return
        
        if result and 'data' in result:
            challenges_data = result['data']
            
            if responses:
                # Show all available fields for first challenge
                if challenges_data:
                    first_challenge = challenges_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Challenges[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_challenge.items()])}",
                        title=f"Challenges - All Fields (First Item, Page {page})"
                    ))
            elif option:
                # Show default table with additional specified fields
                table = Table(title=f"Challenges (Page {page})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Category", style="yellow")
                table.add_column("Difficulty", style="magenta")
                table.add_column("Rating", style="blue")
                table.add_column("Solves", style="red")
                
                # Add additional columns for specified fields
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for challenge in challenges_data:
                    # Default row data
                    row = [
                        str(challenge.get('id', 'N/A') or 'N/A'),
                        str(challenge.get('name', 'N/A') or 'N/A'),
                        str(challenge.get('category_name', 'N/A') or 'N/A'),
                        str(challenge.get('difficulty', 'N/A') or 'N/A'),
                        str(challenge.get('rating', 'N/A') or 'N/A'),
                        str(challenge.get('solves', 'N/A') or 'N/A')
                    ]
                    
                    # Add additional specified fields
                    for field in option:
                        row.append(str(challenge.get(field, 'N/A') or 'N/A'))
                    
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title=f"Challenges (Page {page})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Category", style="yellow")
                table.add_column("Difficulty", style="magenta")
                table.add_column("Rating", style="blue")
                table.add_column("Solves", style="red")
                
                try:
                    for challenge in challenges_data:
                        table.add_row(
                            str(challenge.get('id', 'N/A') or 'N/A'),
                            str(challenge.get('name', 'N/A') or 'N/A'),
                            str(challenge.get('category_name', 'N/A') or 'N/A'),
                            str(challenge.get('difficulty', 'N/A') or 'N/A'),
                            str(challenge.get('rating', 'N/A') or 'N/A'),
                            str(challenge.get('solves', 'N/A') or 'N/A')
                        )
                    
                    console.print(table)
                except Exception as e:
                    console.print(f"[yellow]Error processing challenges data: {e}[/yellow]")
        else:
            console.print("[yellow]No challenges found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_slug')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def info(challenge_slug, responses, option, debug, json_output):
    """Get challenge info by slug"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_info(challenge_slug)
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Challenge Info", json_output)
            return
        
        if result and ('info' in result or 'challenge' in result):
            info = result.get('info') or result.get('challenge')
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for Challenge Info[/bold green]\n"
                    f"{chr(10).join([f'{k}: {v}' for k, v in info.items()])}",
                    title=f"Challenge: {challenge_slug} - All Fields"
                ))
            elif option:
                # Show only specified fields
                selected_info = {}
                for field in option:
                    if field in info:
                        selected_info[field] = info[field]
                    else:
                        console.print(f"[yellow]Field '{field}' not found in response[/yellow]")
                
                if selected_info:
                    console.print(Panel.fit(
                        f"[bold green]Selected Fields[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in selected_info.items()])}",
                        title=f"Challenge: {challenge_slug} - Selected Fields"
                    ))
            else:
                # Default view with enhanced information including play_methods and play_info
                output_lines = [
                    f"[bold green]Challenge Info[/bold green]",
                    f"Name: {info.get('name', 'N/A') or 'N/A'}",
                    f"Category: {info.get('category_name', 'N/A') or 'N/A'}",
                    f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}",
                    f"Stars: {info.get('stars', 'N/A') or 'N/A'}",
                    f"Points: {info.get('points', 'N/A') or 'N/A'}",
                    f"Solves: {info.get('solves', 'N/A') or 'N/A'}",
                    f"Reviews Count: {info.get('reviews_count', 'N/A') or 'N/A'}",
                    f"State: {info.get('state', 'N/A') or 'N/A'}",
                    f"Release Date: {info.get('release_date', 'N/A') or 'N/A'}",
                    f"Description: {info.get('description', 'N/A') or 'N/A'}"
                ]
                
                # Add play_methods if available
                play_methods = info.get('play_methods')
                if play_methods:
                    output_lines.extend([
                        "",
                        f"[bold cyan]Play Methods:[/bold cyan]"
                    ])
                    if isinstance(play_methods, list):
                        for i, method in enumerate(play_methods, 1):
                            output_lines.append(f"  {i}. {method}")
                    else:
                        output_lines.append(f"  {play_methods}")
                
                # Add play_info if available
                play_info = info.get('play_info')
                if play_info:
                    output_lines.extend([
                        "",
                        f"[bold yellow]Play Information:[/bold yellow]"
                    ])
                    if isinstance(play_info, dict):
                        for key, value in play_info.items():
                            # Format the key nicely
                            formatted_key = key.replace('_', ' ').title()
                            if isinstance(value, dict):
                                output_lines.append(f"  [bold]{formatted_key}:[/bold]")
                                for sub_key, sub_value in value.items():
                                    formatted_sub_key = sub_key.replace('_', ' ').title()
                                    output_lines.append(f"    {formatted_sub_key}: {sub_value}")
                            elif isinstance(value, list):
                                output_lines.append(f"  [bold]{formatted_key}:[/bold]")
                                for item in value:
                                    output_lines.append(f"    • {item}")
                            else:
                                output_lines.append(f"  {formatted_key}: {value}")
                    elif isinstance(play_info, list):
                        for i, item in enumerate(play_info, 1):
                            output_lines.append(f"  {i}. {item}")
                    else:
                        output_lines.append(f"  {play_info}")
                
                console.print(Panel.fit(
                    "\n".join(output_lines),
                    title=f"Challenge: {challenge_slug}"
                ))
        else:
            console.print("[yellow]Challenge not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
@click.argument('challenge_identifier')
@click.argument('flag', required=False)
def submit(challenge_identifier, flag, debug, json_output):
    """Submit flag for challenge (accepts challenge ID or name). Flag can be provided as argument or piped from stdin."""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Resolve challenge identifier to challenge ID
        challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
        if challenge_id is None:
            console.print(f"[red]Could not resolve challenge identifier: {challenge_identifier}[/red]")
            return
        
        # Get challenge info to get difficulty
        challenge_info = challenges_module.get_challenge_info(str(challenge_id))
        if not challenge_info or ('info' not in challenge_info and 'challenge' not in challenge_info):
            console.print(f"[red]Could not get challenge info for ID: {challenge_id}[/red]")
            return
        
        info = challenge_info.get('info') or challenge_info.get('challenge')
        difficulty = info.get('difficulty')
        if difficulty is None:
            console.print(f"[red]Could not get difficulty for challenge ID: {challenge_id}[/red]")
            return
        
        # Convert difficulty string to integer if needed
        if isinstance(difficulty, str):
            difficulty_map = {
                'Very Easy': 10,
                'Easy': 20,
                'Medium': 30,
                'Hard': 40,
                'Insane': 50
            }
            difficulty = difficulty_map.get(difficulty, 30)  # Default to Medium if unknown
        
        # Get flag from argument or stdin
        if flag is None:
            # Read from stdin
            if not sys.stdin.isatty():
                flag = sys.stdin.read().strip()
                if not flag:
                    console.print("[red]No flag provided via stdin[/red]")
                    return
            else:
                console.print("[red]No flag provided. Use: htbcli challenges submit <challenge> <flag> or pipe flag via stdin[/red]")
                return
        
        result = challenges_module.submit_challenge_flag(flag, challenge_id, difficulty)
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Challenge Flag Submission", json_output)
            return
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Flag Submission Result[/bold green]\n"
                f"Challenge ID: {challenge_id}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Flag Submission"
            ))
        else:
            console.print("[yellow]No result from flag submission[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def categories(responses, option, debug, json_output):
    """Get challenge categories"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_categories_list()
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Challenge Categories", json_output)
            return
        
        if result and ('data' in result or 'info' in result):
            categories_data = result.get('data') or result.get('info')
            
            if responses:
                # Show all available fields for first category
                if categories_data:
                    first_category = categories_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Challenge Categories[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_category.items()])}",
                        title="Challenge Categories - All Fields (First Item)"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title="Challenge Categories - Selected Fields")
                table.add_column("ID", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for category in categories_data:
                    row = [str(category.get('id', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(category.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title="Challenge Categories")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Description", style="yellow")
                table.add_column("Count", style="magenta")
                
                for category in categories_data:
                    table.add_row(
                        str(category.get('id', 'N/A') or 'N/A'),
                        str(category.get('name', 'N/A') or 'N/A'),
                        str(category.get('description', 'N/A') or 'N/A'),
                        str(category.get('count', 'N/A') or 'N/A')
                    )
                
                console.print(table)
        else:
            console.print("[yellow]No categories found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def recommended(responses, option):
    """Get recommended challenges"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
            if responses:
                # Show all available fields for first recommended challenge
                if recommended_data:
                    first_challenge = recommended_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Recommended Challenges[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_challenge.items()])}",
                        title="Recommended Challenges - All Fields (First Item)"
                    ))
            elif option:
                # Show default table with additional specified fields
                table = Table(title="Recommended Challenges")
                table.add_column("Name", style="cyan")
                table.add_column("Category", style="green")
                table.add_column("Difficulty", style="yellow")
                table.add_column("Points", style="magenta")
                
                # Add additional columns for specified fields
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for challenge in recommended_data:
                    # Default row data
                    row = [
                        str(challenge.get('name', 'N/A') or 'N/A'),
                        str(challenge.get('category', 'N/A') or 'N/A'),
                        str(challenge.get('difficulty', 'N/A') or 'N/A'),
                        str(challenge.get('points', 'N/A') or 'N/A')
                    ]
                    
                    # Add additional specified fields
                    for field in option:
                        row.append(str(challenge.get(field, 'N/A') or 'N/A'))
                    
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title="Recommended Challenges")
                table.add_column("Name", style="cyan")
                table.add_column("Category", style="green")
                table.add_column("Difficulty", style="yellow")
                table.add_column("Points", style="magenta")
                
                for challenge in recommended_data:
                    table.add_row(
                        str(challenge.get('name', 'N/A') or 'N/A'),
                        str(challenge.get('category', 'N/A') or 'N/A'),
                        str(challenge.get('difficulty', 'N/A') or 'N/A'),
                        str(challenge.get('points', 'N/A') or 'N/A')
                    )
                
                console.print(table)
        else:
            console.print("[yellow]No recommended challenges found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def suggested(responses, option):
    """Get suggested challenges"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_suggested()
        
        if result and 'data' in result:
            suggested_data = result['data']
            
            if responses:
                # Show all available fields for first suggested challenge
                if suggested_data:
                    first_challenge = suggested_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Suggested Challenges[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_challenge.items()])}",
                        title="Suggested Challenges - All Fields (First Item)"
                    ))
            elif option:
                # Show default table with additional specified fields
                table = Table(title="Suggested Challenges")
                table.add_column("Name", style="cyan")
                table.add_column("Category", style="green")
                table.add_column("Difficulty", style="yellow")
                table.add_column("Points", style="magenta")
                
                # Add additional columns for specified fields
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for challenge in suggested_data:
                    # Default row data
                    row = [
                        str(challenge.get('name', 'N/A') or 'N/A'),
                        str(challenge.get('category', 'N/A') or 'N/A'),
                        str(challenge.get('difficulty', 'N/A') or 'N/A'),
                        str(challenge.get('points', 'N/A') or 'N/A')
                    ]
                    
                    # Add additional specified fields
                    for field in option:
                        row.append(str(challenge.get(field, 'N/A') or 'N/A'))
                    
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title="Suggested Challenges")
                table.add_column("Name", style="cyan")
                table.add_column("Category", style="green")
                table.add_column("Difficulty", style="yellow")
                table.add_column("Points", style="magenta")
                
                for challenge in suggested_data:
                    table.add_row(
                        str(challenge.get('name', 'N/A') or 'N/A'),
                        str(challenge.get('category', 'N/A') or 'N/A'),
                        str(challenge.get('difficulty', 'N/A') or 'N/A'),
                        str(challenge.get('points', 'N/A') or 'N/A')
                    )
                
                console.print(table)
        else:
            console.print("[yellow]No suggested challenges found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_identifier')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def activity(challenge_identifier, responses, option):
    """Get challenge activity"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Resolve challenge identifier to ID
        challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
        if challenge_id is None:
            return
            
        result = challenges_module.get_challenge_activity(challenge_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            if responses:
                # Show all available fields for first activity
                if activity_data:
                    first_activity = activity_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Challenge Activity[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_activity.items()])}",
                        title=f"Challenge Activity - All Fields (First Item, ID: {challenge_id})"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title=f"Challenge Activity - Selected Fields (ID: {challenge_id})")
                table.add_column("User", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for activity in activity_data:
                    row = [str(activity.get('user', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(activity.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title=f"Challenge Activity (ID: {challenge_id})")
                table.add_column("User", style="cyan")
                table.add_column("Type", style="green")
                table.add_column("Date", style="yellow")
                table.add_column("Points", style="magenta")
                
                for activity in activity_data:
                    table.add_row(
                        str(activity.get('user', 'N/A') or 'N/A'),
                        str(activity.get('type', 'N/A') or 'N/A'),
                        str(activity.get('date', 'N/A') or 'N/A'),
                        str(activity.get('points', 'N/A') or 'N/A')
                    )
                
                console.print(table)
        else:
            console.print("[yellow]No activity found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_identifier')
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def changelog(challenge_identifier, responses, option):
    """Get challenge changelog"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Resolve challenge identifier to ID
        challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
        if challenge_id is None:
            return
            
        result = challenges_module.get_challenge_changelog(challenge_id)
        
        if result and 'data' in result:
            changelog_data = result['data']
            
            if responses:
                # Show all available fields for first changelog entry
                if changelog_data:
                    first_change = changelog_data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields for Challenge Changelog[/bold green]\n"
                        f"{chr(10).join([f'{k}: {v}' for k, v in first_change.items()])}",
                        title=f"Challenge Changelog - All Fields (First Item, ID: {challenge_id})"
                    ))
            elif option:
                # Show only specified fields
                table = Table(title=f"Challenge Changelog - Selected Fields (ID: {challenge_id})")
                table.add_column("Date", style="cyan")
                for field in option:
                    table.add_column(field.title(), style="green")
                
                for change in changelog_data:
                    row = [str(change.get('date', 'N/A') or 'N/A')]
                    for field in option:
                        row.append(str(change.get(field, 'N/A') or 'N/A'))
                    table.add_row(*row)
                
                console.print(table)
            else:
                # Default view
                table = Table(title=f"Challenge Changelog (ID: {challenge_id})")
                table.add_column("Date", style="cyan")
                table.add_column("Type", style="green")
                table.add_column("Description", style="yellow")
                
                for change in changelog_data:
                    table.add_row(
                        str(change.get('date', 'N/A') or 'N/A'),
                        str(change.get('type', 'N/A') or 'N/A'),
                        str(change.get('description', 'N/A') or 'N/A')
                    )
                
                console.print(table)
        else:
            console.print("[yellow]No changelog found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_id', type=int)
@click.option('--output', '-o', help='Output filename for the downloaded file')
def download(challenge_id, output):
    """Download challenge files"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_download(challenge_id)
        
        if result:
            # Generate filename if not provided
            if not output:
                output = f"challenge_{challenge_id}.zip"
            
            # Write binary data to file
            with open(output, 'wb') as f:
                f.write(result)
            
            console.print(Panel.fit(
                f"[bold green]Challenge Download Successful[/bold green]\n"
                f"Challenge ID: {challenge_id}\n"
                f"File saved as: {output}\n"
                f"Size: {len(result)} bytes",
                title="Challenge Download"
            ))
        else:
            console.print("[yellow]No download result[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def start(challenge_identifier, debug, json_output):
    """Start a challenge"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Resolve challenge identifier to ID
        challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
        if challenge_id is None:
            return
            
        result = challenges_module.start_challenge(challenge_id)
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: Challenge Start", json_output)
            return
        
        if result:
            # Get challenge details to show more information
            challenge_info = challenges_module.get_challenge_info_by_id(challenge_id)
            

            
            # Build the output panel with challenge details
            output_lines = [
                f"[bold green]Challenge Start[/bold green]",
                f"Challenge ID: {challenge_id}",
                f"Instance ID: {result.get('id', 'N/A') or 'N/A'}",
                f"Status: {result.get('status', 'N/A') or 'N/A'}",
                f"Message: {result.get('message', 'N/A') or 'N/A'}"
            ]
            
            # Add challenge details if available
            if challenge_info:
                # Check if it has 'challenge' key (from challenge info API) or 'data' key (from challenges list)
                if 'challenge' in challenge_info:
                    challenge_data = challenge_info['challenge']
                elif 'data' in challenge_info:
                    challenge_data = challenge_info['data']
                else:
                    challenge_data = challenge_info
                output_lines.extend([
                    "",
                    f"[bold cyan]Challenge Details:[/bold cyan]",
                    f"Name: {challenge_data.get('name', 'N/A') or 'N/A'}",
                    f"Difficulty: {challenge_data.get('difficulty', 'N/A') or 'N/A'}",
                    f"Category: {challenge_data.get('category_name', 'N/A') or 'N/A'}",
                    f"Points: {challenge_data.get('points', 'N/A') or 'N/A'}",
                    f"State: {challenge_data.get('state', 'N/A') or 'N/A'}"
                ])
                
                # Add Docker connection details if it's a Docker challenge
                if challenge_data.get('docker'):
                    output_lines.extend([
                        "",
                        f"[bold yellow]Docker Connection Information:[/bold yellow]",
                        f"IP: {challenge_data.get('docker_ip', 'N/A') or 'N/A'}",
                        f"Ports: {challenge_data.get('docker_ports', 'N/A') or 'N/A'}",
                        f"Docker Status: {challenge_data.get('docker_status', 'N/A') or 'N/A'}"
                    ])
            
            console.print(Panel.fit(
                "\n".join(output_lines),
                title="Challenge Start"
            ))
        else:
            console.print("[yellow]No start result[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def stop(challenge_identifier, debug, json_output):
    """Stop a challenge"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Resolve challenge identifier to ID
        challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
        if challenge_id is None:
            return
            
        result = challenges_module.stop_challenge(challenge_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Challenge Stop[/bold green]\n"
                f"Challenge ID: {challenge_id}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Challenge Stop"
            ))
        else:
            console.print("[yellow]No stop result[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_identifier', required=False)
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def active(challenge_identifier, debug, json_output):
    """Show active challenge instances or check if a specific challenge is active
    
    If no challenge identifier is provided, it will search through challenges to find active instances.
    Note: This may hit API rate limits when checking all challenges. For best results, specify a challenge name/ID.
    
    Examples:
    - htbcli challenges active "resourcehub core"  # Check specific challenge
    - htbcli challenges active                     # Check all (may hit rate limits)
    """
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        if challenge_identifier:
            # Check if a specific challenge is active
            challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
            if challenge_id is None:
                return
            
            challenge_info = challenges_module.get_challenge_info_by_id(challenge_id)
            
            if debug or json_output:
                handle_debug_option(debug, challenge_info, "Debug: Challenge Info", json_output)
                return
            
            if challenge_info and 'challenge' in challenge_info:
                challenge_data = challenge_info['challenge']
                
                if challenge_data.get('docker_status') == 'ready' and challenge_data.get('docker_ip'):
                    console.print(Panel.fit(
                        f"[bold green]Active Challenge Instance[/bold green]\n"
                        f"Challenge ID: {challenge_id}\n"
                        f"Name: {challenge_data.get('name', 'N/A')}\n"
                        f"Difficulty: {challenge_data.get('difficulty', 'N/A')}\n"
                        f"Category: {challenge_data.get('category_name', 'N/A')}\n"
                        f"IP: {challenge_data.get('docker_ip', 'N/A')}\n"
                        f"Ports: {challenge_data.get('docker_ports', 'N/A')}\n"
                        f"Status: {challenge_data.get('docker_status', 'N/A')}",
                        title="Active Challenge"
                    ))
                else:
                    console.print("[yellow]No active instance found for this challenge[/yellow]")
            else:
                console.print("[red]Could not retrieve challenge information[/red]")
        else:
            # Show all active challenges (limited to avoid rate limits)
            active_challenges = challenges_module.get_active_challenges()
            
            if debug or json_output:
                handle_debug_option(debug, {'active_challenges': active_challenges}, "Debug: Active Challenges", json_output)
                return
            
            if active_challenges:
                table = Table(title="Active Challenge Instances")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Difficulty", style="yellow")
                table.add_column("Category", style="magenta")
                table.add_column("IP", style="blue")
                table.add_column("Ports", style="red")
                table.add_column("Status", style="white")
                
                for challenge in active_challenges:
                    ports_str = ', '.join(map(str, challenge['ports'])) if challenge['ports'] else 'N/A'
                    table.add_row(
                        str(challenge['id']),
                        challenge['name'],
                        challenge['difficulty'],
                        challenge['category'],
                        challenge['ip'],
                        ports_str,
                        challenge['status']
                    )
                
                console.print(table)
            else:
                console.print("[yellow]No active challenge instances found[/yellow]")
                
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def writeup(challenge_identifier, debug, json_output):
    """Get challenge writeup"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Resolve challenge identifier to ID
        challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
        if challenge_id is None:
            return
            
        result = challenges_module.get_challenge_writeup(challenge_id)
        
        if result and 'data' in result and 'official' in result['data']:
            writeup_data = result['data']['official']
            
            console.print(Panel.fit(
                f"[bold green]Challenge Writeup[/bold green]\n"
                f"Challenge ID: {challenge_id}\n"
                f"Filename: {writeup_data.get('filename', 'N/A') or 'N/A'}\n"
                f"SHA256: {writeup_data.get('sha256', 'N/A') or 'N/A'}\n"
                f"URL: {writeup_data.get('url', 'N/A') or 'N/A'}\n"
                f"Video URL: {writeup_data.get('video_url', 'N/A') or 'N/A'}",
                title="Challenge Writeup"
            ))
        else:
            console.print("[yellow]No writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_identifier')
@click.option('--output', '-o', help='Output filename for the downloaded file')
def writeup_official(challenge_identifier, output):
    """Get official challenge writeup"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Resolve challenge identifier to ID
        challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
        if challenge_id is None:
            return
            
        result = challenges_module.get_challenge_writeup_official(challenge_id)
        
        if result:
            # Generate filename if not provided
            if not output:
                output = f"challenge_{challenge_id}_writeup_official.pdf"
            
            # Write binary data to file
            with open(output, 'wb') as f:
                f.write(result)
            
            console.print(Panel.fit(
                f"[bold green]Official Challenge Writeup Downloaded[/bold green]\n"
                f"Challenge ID: {challenge_id}\n"
                f"File saved as: {output}\n"
                f"Size: {len(result)} bytes",
                title="Official Challenge Writeup"
            ))
        else:
            console.print("[yellow]No official writeup found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')

@click.argument('review_id', type=int)
def mark_helpful(review_id, debug, json_output):
    """Mark review as helpful"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.mark_review_helpful(review_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Mark Review Helpful[/bold green]\n"
                f"Review ID: {review_id}\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Mark Review Helpful"
            ))
        else:
            console.print("[yellow]No result from marking review helpful[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_name')
@click.option('--max-pages', default=5, help='Maximum number of pages to search')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def search(challenge_name, max_pages, debug, json_output):
    """Search for a challenge by name"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        challenge_id = challenges_module.search_challenge_by_name(challenge_name, max_pages)
        
        if challenge_id:
            console.print(Panel.fit(
                f"[bold green]Challenge Found[/bold green]\n"
                f"Name: {challenge_name}\n"
                f"ID: {challenge_id}",
                title="Challenge Search Result"
            ))
        else:
            console.print(f"[yellow]No challenge found with name: {challenge_name}[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('challenge_identifier')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def reviews_user(challenge_identifier, debug, json_output):
    """Get user's review for challenge"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        
        # Resolve challenge identifier to ID
        challenge_id = challenges_module.resolve_challenge_id(challenge_identifier)
        if challenge_id is None:
            return
            
        result = challenges_module.get_challenge_reviews_user(challenge_id)
        
        if result and 'data' in result:
            reviews_data = result['data']
            
            table = Table(title=f"User Reviews for Challenge (ID: {challenge_id})")
            table.add_column("Review ID", style="cyan")
            table.add_column("Rating", style="green")
            table.add_column("Comment", style="yellow")
            table.add_column("Date", style="magenta")
            
            for review in reviews_data:
                table.add_row(
                    str(review.get('id', 'N/A') or 'N/A'),
                    str(review.get('rating', 'N/A') or 'N/A'),
                    str(review.get('comment', 'N/A') or 'N/A'),
                    str(review.get('date', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No user reviews found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
