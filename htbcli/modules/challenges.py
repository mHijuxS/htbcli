"""
Challenges module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

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
    
    def get_challenge_download(self, challenge_id: int) -> Dict[str, Any]:
        """Download challenge files"""
        return self.api.get(f"/challenge/download/{challenge_id}")
    
    def get_challenge_info(self, challenge_slug: str) -> Dict[str, Any]:
        """Get challenge info by slug"""
        return self.api.get(f"/challenge/info/{challenge_slug}")
    
    def submit_challenge_flag(self, flag: str) -> Dict[str, Any]:
        """Submit flag for challenge"""
        return self.api.post("/challenge/own", json_data={"flag": flag})
    
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
    
    def get_challenge_writeup_official(self, challenge_id: int) -> Dict[str, Any]:
        """Get official challenge writeup"""
        return self.api.get(f"/challenge/{challenge_id}/writeup/official")
    
    def get_challenges(self, page: int = 1, per_page: int = 20, difficulty: Optional[str] = None, category: Optional[str] = None) -> Dict[str, Any]:
        """Get list of challenges"""
        params = {
            "page": page,
            "per_page": per_page
        }
        if difficulty:
            params["difficulty"] = difficulty
        if category:
            params["category"] = category
        return self.api.get("/challenges", params=params)
    
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
@click.option('--difficulty', type=click.Choice(['Easy', 'Medium', 'Hard', 'Insane']), help='Challenge difficulty')
@click.option('--category', help='Challenge category')
def list(page, per_page, difficulty, category):
    """List challenges"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenges(page, per_page, difficulty, category)
        
        if result and 'data' in result:
            challenges_data = result['data']['data'] if isinstance(result['data'], dict) and 'data' in result['data'] else result['data']
            
            table = Table(title=f"Challenges (Page {page})")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Category", style="yellow")
            table.add_column("Difficulty", style="magenta")
            table.add_column("Points", style="blue")
            table.add_column("Solves", style="red")
            
            try:
                for challenge in challenges_data:
                    table.add_row(
                        str(challenge.get('id', 'N/A') or 'N/A'),
                        str(challenge.get('name', 'N/A') or 'N/A'),
                        str(challenge.get('category', 'N/A') or 'N/A'),
                        str(challenge.get('difficulty', 'N/A') or 'N/A'),
                        str(challenge.get('points', 'N/A') or 'N/A'),
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
def info(challenge_slug):
    """Get challenge info by slug"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_info(challenge_slug)
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]Challenge Info[/bold green]\n"
                f"Name: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Category: {info.get('category', 'N/A') or 'N/A'}\n"
                f"Difficulty: {info.get('difficulty', 'N/A') or 'N/A'}\n"
                f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                f"Solves: {info.get('solves', 'N/A') or 'N/A'}\n"
                f"Description: {info.get('description', 'N/A') or 'N/A'}",
                title=f"Challenge: {challenge_slug}"
            ))
        else:
            console.print("[yellow]Challenge not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
@click.argument('flag')
def submit(flag):
    """Submit flag for challenge"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.submit_challenge_flag(flag)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Flag Submission Result[/bold green]\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Flag Submission"
            ))
        else:
            console.print("[yellow]No result from flag submission[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@challenges.command()
def categories():
    """Get challenge categories"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_categories_list()
        
        if result and 'data' in result:
            categories_data = result['data']
            
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
def recommended():
    """Get recommended challenges"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_recommended()
        
        if result and 'data' in result:
            recommended_data = result['data']
            
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
def suggested():
    """Get suggested challenges"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_suggested()
        
        if result and 'data' in result:
            suggested_data = result['data']
            
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
@click.argument('challenge_id', type=int)
def activity(challenge_id):
    """Get challenge activity"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_activity(challenge_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
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
@click.argument('challenge_id', type=int)
def changelog(challenge_id):
    """Get challenge changelog"""
    try:
        api_client = HTBAPIClient()
        challenges_module = ChallengesModule(api_client)
        result = challenges_module.get_challenge_changelog(challenge_id)
        
        if result and 'data' in result:
            changelog_data = result['data']
            
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
