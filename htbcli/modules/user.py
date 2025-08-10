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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def info(responses, option):
    """Get user information"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_info()
        
        if result and 'info' in result:
            info = result['info']
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All Available Fields for User Info[/bold green]\n"
                    f"{chr(10).join([f'{k}: {v}' for k, v in info.items()])}",
                    title="User Info - All Fields"
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
                        title="User Info - Selected Fields"
                    ))
            else:
                # Default view with enhanced information
                team_name = info.get('team', {}).get('name', 'N/A') if info.get('team') else 'N/A'
                console.print(Panel.fit(
                    f"[bold green]User Information[/bold green]\n"
                    f"Username: {info.get('name', 'N/A') or 'N/A'}\n"
                    f"Email: {info.get('email', 'N/A') or 'N/A'}\n"
                    f"Rank ID: {info.get('rank_id', 'N/A') or 'N/A'}\n"
                    f"Team: {team_name}\n"
                    f"VIP: {'Yes' if info.get('isVip') else 'No'}\n"
                    f"Subscription: {info.get('subscriptionType', 'N/A') or 'N/A'}\n"
                    f"Verified: {'Yes' if info.get('verified') else 'No'}\n"
                    f"Timezone: {info.get('timezone', 'N/A') or 'N/A'}\n"
                    f"Server ID: {info.get('server_id', 'N/A') or 'N/A'}\n"
                    f"Beta Tester: {'Yes' if info.get('beta_tester') else 'No'}",
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
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def dashboard(responses, option):
    """Get user dashboard"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_dashboard()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Dashboard Data[/bold green]\n"
                    f"{result}",
                    title="User Dashboard"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Dashboard[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="User Dashboard"))
            else:
                # Show default fields
                if 'dashboard_players' in result:
                    dashboard_data = result['dashboard_players']
                    console.print(Panel.fit(
                        f"[bold green]User Dashboard[/bold green]\n"
                        f"Online Players: {dashboard_data.get('online_players', 'N/A') or 'N/A'}",
                        title="Dashboard"
                    ))
                else:
                    console.print(Panel.fit(
                        f"[bold green]User Dashboard[/bold green]\n"
                        f"Data available: Yes",
                        title="Dashboard"
                    ))
        else:
            console.print("[yellow]No dashboard data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def followers(responses, option):
    """Get user followers"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_followers()
        
        if result and 'info' in result:
            followers_data = result['info']
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Followers Data[/bold green]\n"
                    f"{result}",
                    title="User Followers"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Followers[/bold green]\n"
                for i, follower in enumerate(followers_data):
                    info_text += f"Follower {i+1}:\n"
                    for field in option:
                        value = follower.get(field, 'N/A')
                        info_text += f"  {field}: {value}\n"
                console.print(Panel.fit(info_text, title="User Followers"))
            else:
                # Show default fields
                if len(followers_data) > 0:
                    table = Table(title="User Followers")
                    table.add_column("ID", style="cyan")
                    
                    for follower in followers_data:
                        table.add_row(
                            str(follower.get('id', 'N/A') or 'N/A')
                        )
                    
                    console.print(table)
                else:
                    console.print(Panel.fit(
                        f"[bold green]User Followers[/bold green]\n"
                        f"Count: {len(followers_data)}",
                        title="User Followers"
                    ))
        else:
            console.print("[yellow]No followers found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def summary(responses, option):
    """Get user profile summary"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_summary()
        
        if result and 'userStats' in result:
            summary_data = result['userStats']
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Summary Data[/bold green]\n"
                    f"{result}",
                    title="User Summary"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Summary[/bold green]\n"
                for field in option:
                    value = summary_data.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="User Summary"))
            else:
                # Show default fields
                team_name = summary_data.get('team', {}).get('name', 'N/A') if summary_data.get('team') else 'N/A'
                console.print(Panel.fit(
                    f"[bold green]User Summary[/bold green]\n"
                    f"Username: {summary_data.get('name', 'N/A') or 'N/A'}\n"
                    f"Rank: {summary_data.get('rank', 'N/A') or 'N/A'}\n"
                    f"Points: {summary_data.get('points', 'N/A') or 'N/A'}\n"
                    f"Team: {team_name}\n"
                    f"System Owns: {summary_data.get('system_owns', 'N/A') or 'N/A'}\n"
                    f"User Owns: {summary_data.get('user_owns', 'N/A') or 'N/A'}\n"
                    f"Respects: {summary_data.get('respects', 'N/A') or 'N/A'}\n"
                    f"Ranking: {summary_data.get('ranking', 'N/A') or 'N/A'}",
                    title="Profile Summary"
                ))
        else:
            console.print("[yellow]No summary found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def settings(responses, option):
    """Get user settings"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_settings()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Settings Data[/bold green]\n"
                    f"{result}",
                    title="User Settings"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Settings[/bold green]\n"
                for field in option:
                    value = result.get(field, 'N/A')
                    info_text += f"{field}: {value}\n"
                console.print(Panel.fit(info_text, title="User Settings"))
            else:
                # Show default fields
                console.print(Panel.fit(
                    f"[bold green]User Settings[/bold green]\n"
                    f"Email: {result.get('email', 'N/A') or 'N/A'}\n"
                    f"Public: {result.get('public', 'N/A') or 'N/A'}\n"
                    f"Name Change Delay: {result.get('name_change_delay', 'N/A') or 'N/A'}\n"
                    f"Hide Machine Tags: {result.get('hide_machine_tags', 'N/A') or 'N/A'}",
                    title="User Settings"
                ))
        else:
            console.print("[yellow]No settings found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def tracks(responses, option):
    """Get user tracks"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_tracks()
        
        if result:
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All User Tracks Data[/bold green]\n"
                    f"{result}",
                    title="User Tracks"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]User Tracks[/bold green]\n"
                for i, track in enumerate(result):
                    info_text += f"Track {i+1}:\n"
                    for field in option:
                        value = track.get(field, 'N/A')
                        info_text += f"  {field}: {value}\n"
                console.print(Panel.fit(info_text, title="User Tracks"))
            else:
                # Show default fields
                if isinstance(result, list) and len(result) > 0:
                    table = Table(title="User Tracks")
                    table.add_column("ID", style="cyan")
                    table.add_column("Complete", style="green")
                    
                    for track in result:
                        table.add_row(
                            str(track.get('id', 'N/A') or 'N/A'),
                            str(track.get('complete', 'N/A') or 'N/A')
                        )
                    
                    console.print(table)
                else:
                    console.print(Panel.fit(
                        f"[bold green]User Tracks[/bold green]\n"
                        f"Count: {len(result) if isinstance(result, list) else 0}",
                        title="User Tracks"
                    ))
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

@user.command()
@click.argument('target_type')
@click.argument('user_id', type=int)
@click.argument('target_id', type=int)
def achievement(target_type, user_id, target_id):
    """Validate achievement/own"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_achievement(target_type, user_id, target_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Achievement Validation[/bold green]\n"
                f"Target Type: {target_type}\n"
                f"User ID: {user_id}\n"
                f"Target ID: {target_id}\n"
                f"Result: {result}",
                title="Achievement Validation"
            ))
        else:
            console.print("[yellow]No achievement data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def anonymized_id():
    """Get user's anonymous ID"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_anonymized_id()
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Anonymous ID[/bold green]\n"
                f"Data: {result}",
                title="Anonymous ID"
            ))
        else:
            console.print("[yellow]No anonymous ID found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.option('--responses', is_flag=True, help='Show all available response fields')
@click.option('-o', '--option', multiple=True, help='Show specific field(s) (can be used multiple times)')
def apptoken_list(responses, option):
    """Get user app tokens list"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_apptoken_list()
        
        if result and 'tokens' in result:
            tokens_data = result['tokens']
            
            if responses:
                # Show all available fields
                console.print(Panel.fit(
                    f"[bold green]All App Tokens Data[/bold green]\n"
                    f"{result}",
                    title="App Tokens"
                ))
            elif option:
                # Show specific fields
                info_text = f"[bold green]App Tokens[/bold green]\n"
                for i, token in enumerate(tokens_data):
                    info_text += f"Token {i+1}:\n"
                    for field in option:
                        value = token.get(field, 'N/A')
                        info_text += f"  {field}: {value}\n"
                console.print(Panel.fit(info_text, title="App Tokens"))
            else:
                # Show default fields
                if len(tokens_data) > 0:
                    table = Table(title="App Tokens")
                    table.add_column("Name", style="cyan")
                    table.add_column("Created", style="green")
                    table.add_column("Expires", style="yellow")
                    table.add_column("Last Seen", style="magenta")
                    
                    for token in tokens_data:
                        table.add_row(
                            str(token.get('name', 'N/A') or 'N/A'),
                            str(token.get('created_at', 'N/A') or 'N/A'),
                            str(token.get('expires_at', 'N/A') or 'N/A'),
                            str(token.get('last_seen', 'N/A') or 'N/A')
                        )
                    
                    console.print(table)
                else:
                    console.print(Panel.fit(
                        f"[bold green]App Tokens[/bold green]\n"
                        f"Count: {len(tokens_data)}",
                        title="App Tokens"
                    ))
        else:
            console.print("[yellow]No app tokens found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def banned():
    """Check if user is banned"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_banned()
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Ban Status[/bold green]\n"
                f"Data: {result}",
                title="Ban Status"
            ))
        else:
            console.print("[yellow]No ban status found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def connection_status():
    """Get user connection status"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_connection_status()
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Connection Status[/bold green]\n"
                f"Data: {result}",
                title="Connection Status"
            ))
        else:
            console.print("[yellow]No connection status found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
def dashboard_tabloid():
    """Get user dashboard tabloid"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_dashboard_tabloid()
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Dashboard Tabloid[/bold green]\n"
                f"Data: {result}",
                title="Dashboard Tabloid"
            ))
        else:
            console.print("[yellow]No dashboard tabloid found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def chart_machines_attack(user_id):
    """Get user profile machine attack chart"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_chart_machines_attack(user_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]Machine Attack Chart[/bold green]\n"
                f"User ID: {user_id}\n"
                f"Data: {result}",
                title="Machine Attack Chart"
            ))
        else:
            console.print("[yellow]No chart data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def content(user_id):
    """Get user profile content"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_content(user_id)
        
        if result and 'profile' in result and 'content' in result['profile']:
            content_data = result['profile']['content']
            
            # Display machines
            if content_data.get('machines'):
                table = Table(title=f"User Machines (ID: {user_id})")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("OS", style="yellow")
                table.add_column("Difficulty", style="magenta")
                table.add_column("Rating", style="blue")
                table.add_column("User Owns", style="red")
                
                for machine in content_data['machines']:
                    table.add_row(
                        str(machine.get('id', 'N/A') or 'N/A'),
                        str(machine.get('name', 'N/A') or 'N/A'),
                        str(machine.get('os', 'N/A') or 'N/A'),
                        str(machine.get('difficulty', 'N/A') or 'N/A'),
                        str(machine.get('rating', 'N/A') or 'N/A'),
                        str(machine.get('user_owns', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            
            # Display challenges if any
            if content_data.get('challenges'):
                table = Table(title=f"User Challenges (ID: {user_id})")
                table.add_column("Name", style="cyan")
                table.add_column("Category", style="green")
                table.add_column("Difficulty", style="yellow")
                
                for challenge in content_data['challenges']:
                    table.add_row(
                        str(challenge.get('name', 'N/A') or 'N/A'),
                        str(challenge.get('category', 'N/A') or 'N/A'),
                        str(challenge.get('difficulty', 'N/A') or 'N/A')
                    )
                
                console.print(table)
            
            # Display writeups if any
            if content_data.get('writeups'):
                table = Table(title=f"User Writeups (ID: {user_id})")
                table.add_column("Title", style="cyan")
                table.add_column("Type", style="green")
                table.add_column("Date", style="yellow")
                
                for writeup in content_data['writeups']:
                    table.add_row(
                        str(writeup.get('title', 'N/A') or 'N/A'),
                        str(writeup.get('type', 'N/A') or 'N/A'),
                        str(writeup.get('date', 'N/A') or 'N/A')
                    )
                
                console.print(table)
        else:
            console.print("[yellow]No content found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('period')
@click.argument('user_id', type=int)
def graph(period, user_id):
    """Get user profile graph"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_graph(period, user_id)
        
        if result:
            console.print(Panel.fit(
                f"[bold green]User Profile Graph[/bold green]\n"
                f"Period: {period}\n"
                f"User ID: {user_id}\n"
                f"Data: {result}",
                title="User Profile Graph"
            ))
        else:
            console.print("[yellow]No graph data found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def progress_challenges(user_id):
    """Get user profile progress challenges"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_progress_challenges(user_id)
        
        if result and 'data' in result:
            progress_data = result['data']
            
            table = Table(title=f"Challenge Progress (ID: {user_id})")
            table.add_column("Category", style="cyan")
            table.add_column("Progress", style="green")
            table.add_column("Total", style="yellow")
            
            for category in progress_data:
                table.add_row(
                    str(category.get('category', 'N/A') or 'N/A'),
                    str(category.get('progress', 'N/A') or 'N/A'),
                    str(category.get('total', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No challenge progress found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def progress_fortress(user_id):
    """Get user profile progress fortress"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_progress_fortress(user_id)
        
        if result and 'data' in result:
            progress_data = result['data']
            
            table = Table(title=f"Fortress Progress (ID: {user_id})")
            table.add_column("Fortress", style="cyan")
            table.add_column("Progress", style="green")
            table.add_column("Total", style="yellow")
            
            for fortress in progress_data:
                table.add_row(
                    str(fortress.get('fortress', 'N/A') or 'N/A'),
                    str(fortress.get('progress', 'N/A') or 'N/A'),
                    str(fortress.get('total', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No fortress progress found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def progress_machines_os(user_id):
    """Get user profile progress machines OS"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_progress_machines_os(user_id)
        
        if result and 'data' in result:
            progress_data = result['data']
            
            table = Table(title=f"Machines OS Progress (ID: {user_id})")
            table.add_column("OS", style="cyan")
            table.add_column("Progress", style="green")
            table.add_column("Total", style="yellow")
            
            for os in progress_data:
                table.add_row(
                    str(os.get('os', 'N/A') or 'N/A'),
                    str(os.get('progress', 'N/A') or 'N/A'),
                    str(os.get('total', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No machines OS progress found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def progress_prolab(user_id):
    """Get user profile progress prolab"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_progress_prolab(user_id)
        
        if result and 'data' in result:
            progress_data = result['data']
            
            table = Table(title=f"ProLab Progress (ID: {user_id})")
            table.add_column("ProLab", style="cyan")
            table.add_column("Progress", style="green")
            table.add_column("Total", style="yellow")
            
            for prolab in progress_data:
                table.add_row(
                    str(prolab.get('prolab', 'N/A') or 'N/A'),
                    str(prolab.get('progress', 'N/A') or 'N/A'),
                    str(prolab.get('total', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No prolab progress found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@user.command()
@click.argument('user_id', type=int)
def progress_sherlocks(user_id):
    """Get user profile progress sherlocks"""
    try:
        api_client = HTBAPIClient()
        user_module = UserModule(api_client)
        result = user_module.get_user_profile_progress_sherlocks(user_id)
        
        if result and 'data' in result:
            progress_data = result['data']
            
            table = Table(title=f"Sherlocks Progress (ID: {user_id})")
            table.add_column("Sherlock", style="cyan")
            table.add_column("Progress", style="green")
            table.add_column("Total", style="yellow")
            
            for sherlock in progress_data:
                table.add_row(
                    str(sherlock.get('sherlock', 'N/A') or 'N/A'),
                    str(sherlock.get('progress', 'N/A') or 'N/A'),
                    str(sherlock.get('total', 'N/A') or 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[yellow]No sherlocks progress found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
