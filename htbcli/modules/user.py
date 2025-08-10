"""
User module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..api_client import HTBAPIClient

console = Console()

class UserModule:
    """Module for handling user-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def get_user_achievement(self, target_type: str, user_id: int, target_id: int) -> Dict[str, Any]:
        """Validate achievement/own"""
        return self.api.get(f"/user/achievement/{target_type}/{user_id}/{target_id}")
    
    def get_user_anonymized_id(self) -> Dict[str, Any]:
        """Get user's anonymous ID"""
        return self.api.get("/user/anonymized/id")
    
    def create_user_apptoken(self, token_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user app token"""
        return self.api.post("/user/apptoken/create", json_data=token_data)
    
    def delete_user_apptoken(self, token_data: Dict[str, Any]) -> Dict[str, Any]:
        """Delete user app token"""
        return self.api.post("/user/apptoken/delete", json_data=token_data)
    
    def get_user_apptoken_list(self) -> Dict[str, Any]:
        """Get user app tokens list"""
        return self.api.get("/user/apptoken/list")
    
    def get_user_banned(self) -> Dict[str, Any]:
        """Check if user is banned"""
        return self.api.get("/user/banned")
    
    def get_user_connection_status(self) -> Dict[str, Any]:
        """Get user connection status"""
        return self.api.get("/user/connection/status")
    
    def get_user_dashboard(self) -> Dict[str, Any]:
        """Get user dashboard"""
        return self.api.get("/user/dashboard")
    
    def get_user_dashboard_tabloid(self) -> Dict[str, Any]:
        """Get user dashboard tabloid"""
        return self.api.get("/user/dashboard/tabloid")
    
    def disrespect_user(self, user_id: int) -> Dict[str, Any]:
        """Disrespect a user"""
        return self.api.post(f"/user/disrespect/{user_id}")
    
    def follow_user(self, user_id: int) -> Dict[str, Any]:
        """Follow a user"""
        return self.api.post(f"/user/follow/{user_id}")
    
    def get_user_followers(self) -> Dict[str, Any]:
        """Get user's followers"""
        return self.api.get("/user/followers")
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user information"""
        return self.api.get("/user/info")
    
    def get_user_profile_activity(self, user_id: int) -> Dict[str, Any]:
        """Get user profile activity"""
        return self.api.get(f"/user/profile/activity/{user_id}")
    
    def get_user_profile_badges(self, user_id: int) -> Dict[str, Any]:
        """Get user profile badges"""
        return self.api.get(f"/user/profile/badges/{user_id}")
    
    def get_user_profile_basic(self, user_id: int) -> Dict[str, Any]:
        """Get user basic profile"""
        return self.api.get(f"/user/profile/basic/{user_id}")
    
    def get_user_profile_bloods(self, user_id: int) -> Dict[str, Any]:
        """Get user profile bloods"""
        return self.api.get(f"/user/profile/bloods/{user_id}")
    
    def get_user_profile_chart_machines_attack(self, user_id: int) -> Dict[str, Any]:
        """Get user profile machine attack chart"""
        return self.api.get(f"/user/profile/chart/machines/attack/{user_id}")
    
    def get_user_profile_content(self, user_id: int) -> Dict[str, Any]:
        """Get user profile content"""
        return self.api.get(f"/user/profile/content/{user_id}")
    
    def get_user_profile_graph(self, period: str, user_id: int) -> Dict[str, Any]:
        """Get user profile graph"""
        return self.api.get(f"/user/profile/graph/{period}/{user_id}")
    
    def get_user_profile_progress_challenges(self, user_id: int) -> Dict[str, Any]:
        """Get user progress challenges"""
        return self.api.get(f"/user/profile/progress/challenges/{user_id}")
    
    def get_user_profile_progress_fortress(self, user_id: int) -> Dict[str, Any]:
        """Get user progress fortress"""
        return self.api.get(f"/user/profile/progress/fortress/{user_id}")
    
    def get_user_profile_progress_machines_os(self, user_id: int) -> Dict[str, Any]:
        """Get user progress machines OS"""
        return self.api.get(f"/user/profile/progress/machines/os/{user_id}")
    
    def get_user_profile_progress_prolab(self, user_id: int) -> Dict[str, Any]:
        """Get user progress prolab"""
        return self.api.get(f"/user/profile/progress/prolab/{user_id}")
    
    def get_user_profile_progress_sherlocks(self, user_id: int) -> Dict[str, Any]:
        """Get user progress sherlocks"""
        return self.api.get(f"/user/profile/progress/sherlocks/{user_id}")
    
    def get_user_profile_summary(self) -> Dict[str, Any]:
        """Get user profile summary"""
        return self.api.get("/user/profile/summary")
    
    def respect_user(self, user_id: int) -> Dict[str, Any]:
        """Respect a user"""
        return self.api.post(f"/user/respect/{user_id}")
    
    def get_user_settings(self) -> Dict[str, Any]:
        """Get user settings"""
        return self.api.get("/user/settings")
    
    def get_user_tracks(self) -> Dict[str, Any]:
        """Get user tracks"""
        return self.api.get("/user/tracks")
    
    def unfollow_user(self, user_id: int) -> Dict[str, Any]:
        """Unfollow a user"""
        return self.api.post(f"/user/unfollow/{user_id}")

# Click commands
@click.group()
def user():
    """User-related commands"""
    pass

@user.command()
def info():
    """Get user information"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_info()
        
        if result and 'info' in result:
            info = result['info']
            console.print(Panel.fit(
                f"[bold green]User Information[/bold green]\n"
                f"Username: {info.get('name', 'N/A') or 'N/A'}\n"
                f"Rank: {info.get('rank', 'N/A') or 'N/A'}\n"
                f"Points: {info.get('points', 'N/A') or 'N/A'}\n"
                f"Country: {info.get('country_name', 'N/A') or 'N/A'}\n"
                f"Member Since: {info.get('member_since', 'N/A') or 'N/A'}",
                title="User Info"
            ))
        else:
            console.print("[yellow]No user info found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def profile(user_id):
    """Get user profile"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_basic(user_id)
        
        if result and 'profile' in result:
            profile = result['profile']
            console.print(Panel.fit(
                f"[bold green]User Profile[/bold green]\n"
                f"Username: {profile.get('name', 'N/A') or 'N/A'}\n"
                f"Rank: {profile.get('rank', 'N/A') or 'N/A'}\n"
                f"Points: {profile.get('points', 'N/A') or 'N/A'}\n"
                f"Country: {profile.get('country_name', 'N/A') or 'N/A'}\n"
                f"Member Since: {profile.get('member_since', 'N/A') or 'N/A'}\n"
                f"Avatar: {profile.get('avatar', 'N/A') or 'N/A'}",
                title=f"User ID: {user_id}"
            ))
        else:
            console.print("[yellow]User not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def activity(user_id):
    """Get user activity"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_activity(user_id)
        
        if result and 'data' in result:
            activity_data = result['data']
            
            table = Table(title=f"User Activity (ID: {user_id})")
            table.add_column("Type", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Date", style="yellow")
            table.add_column("Points", style="magenta")
            
            for activity in activity_data:
                table.add_row(
                    str(activity.get('type', 'N/A') or 'N/A'),
                    str(activity.get('name', 'N/A') or 'N/A'),
                    str(activity.get('date', 'N/A') or 'N/A'),
                    str(activity.get('points', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No activity found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def badges(user_id):
    """Get user badges"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_badges(user_id)
        
        if result and 'data' in result:
            badges_data = result['data']
            
            table = Table(title=f"User Badges (ID: {user_id})")
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="green")
            table.add_column("Date", style="yellow")
            table.add_column("Icon", style="magenta")
            
            for badge in badges_data:
                table.add_row(
                    str(badge.get('name', 'N/A') or 'N/A'),
                    str(badge.get('description', 'N/A') or 'N/A'),
                    str(badge.get('date', 'N/A') or 'N/A'),
                    str(badge.get('icon', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No badges found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def bloods(user_id):
    """Get user bloods"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_bloods(user_id)
        
        if result and 'data' in result:
            bloods_data = result['data']
            
            table = Table(title=f"User Bloods (ID: {user_id})")
            table.add_column("Machine", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Date", style="yellow")
            table.add_column("Position", style="magenta")
            
            for blood in bloods_data:
                table.add_row(
                    str(blood.get('machine', 'N/A') or 'N/A'),
                    str(blood.get('type', 'N/A') or 'N/A'),
                    str(blood.get('date', 'N/A') or 'N/A'),
                    str(blood.get('position', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No bloods found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def dashboard():
    """Get user dashboard"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_dashboard()
        
        if result and 'data' in result:
            dashboard_data = result['data']
            console.print(Panel.fit(
                f"[bold green]User Dashboard[/bold green]\n"
                f"Rank: {dashboard_data.get('rank', 'N/A') or 'N/A'}\n"
                f"Points: {dashboard_data.get('points', 'N/A') or 'N/A'}\n"
                f"Machines Owned: {dashboard_data.get('machines_owned', 'N/A') or 'N/A'}\n"
                f"Challenges Solved: {dashboard_data.get('challenges_solved', 'N/A') or 'N/A'}",
                title="Dashboard"
            ))
        else:
            console.print("[yellow]No dashboard data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def followers():
    """Get user followers"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_followers()
        
        if result and 'data' in result:
            followers_data = result['data']
            
            table = Table(title="User Followers")
            table.add_column("Username", style="cyan")
            table.add_column("Rank", style="green")
            table.add_column("Points", style="yellow")
            table.add_column("Country", style="magenta")
            
            for follower in followers_data:
                table.add_row(
                    str(follower.get('name', 'N/A') or 'N/A'),
                    str(follower.get('rank', 'N/A') or 'N/A'),
                    str(follower.get('points', 'N/A') or 'N/A'),
                    str(follower.get('country_name', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No followers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def summary():
    """Get user profile summary"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_summary()
        
        if result and 'data' in result:
            summary_data = result['data']
            console.print(Panel.fit(
                f"[bold green]User Summary[/bold green]\n"
                f"Username: {summary_data.get('name', 'N/A') or 'N/A'}\n"
                f"Rank: {summary_data.get('rank', 'N/A') or 'N/A'}\n"
                f"Points: {summary_data.get('points', 'N/A') or 'N/A'}\n"
                f"Country: {summary_data.get('country_name', 'N/A') or 'N/A'}\n"
                f"Member Since: {summary_data.get('member_since', 'N/A') or 'N/A'}",
                title="Profile Summary"
            ))
        else:
            console.print("[yellow]No summary found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def settings():
    """Get user settings"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_settings()
        
        if result and 'data' in result:
            settings_data = result['data']
            console.print(Panel.fit(
                f"[bold green]User Settings[/bold green]\n"
                f"Email: {settings_data.get('email', 'N/A') or 'N/A'}\n"
                f"Timezone: {settings_data.get('timezone', 'N/A') or 'N/A'}\n"
                f"Language: {settings_data.get('language', 'N/A') or 'N/A'}",
                title="Settings"
            ))
        else:
            console.print("[yellow]No settings found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def tracks():
    """Get user tracks"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_tracks()
        
        if result and 'data' in result:
            tracks_data = result['data']
            
            table = Table(title="User Tracks")
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="green")
            table.add_column("Progress", style="yellow")
            table.add_column("Enrolled", style="magenta")
            
            for track in tracks_data:
                table.add_row(
                    str(track.get('name', 'N/A') or 'N/A'),
                    str(track.get('description', 'N/A') or 'N/A'),
                    str(track.get('progress', 'N/A') or 'N/A'),
                    str(track.get('enrolled', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No tracks found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def follow(user_id):
    """Follow a user"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.follow_user(user_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Follow Result[/bold green]\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Follow User"
            ))
        else:
            console.print("[yellow]No result from follow action[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def unfollow(user_id):
    """Unfollow a user"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.unfollow_user(user_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Unfollow Result[/bold green]\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Unfollow User"
            ))
        else:
            console.print("[yellow]No result from unfollow action[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def respect(user_id):
    """Respect a user"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.respect_user(user_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Respect Result[/bold green]\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Respect User"
            ))
        else:
            console.print("[yellow]No result from respect action[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def disrespect(user_id):
    """Disrespect a user"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.disrespect_user(user_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Disrespect Result[/bold green]\n"
                f"Status: {result.get('status', 'N/A') or 'N/A'}\n"
                f"Message: {result.get('message', 'N/A') or 'N/A'}",
                title="Disrespect User"
            ))
        else:
            console.print("[yellow]No result from disrespect action[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
