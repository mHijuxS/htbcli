"""
PwnBox module for HTB CLI
"""

import click
from typing import Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from ..api_client import HTBAPIClient
from ..base_command import handle_debug_option

console = Console()

class PwnBoxModule:
    """Module for handling PwnBox-related API calls"""
    
    def __init__(self, api_client: HTBAPIClient):
        self.api = api_client
    
    def start_pwnbox(self, location: str) -> Dict[str, Any]:
        """Start a PwnBox instance"""
        return self.api.post("/pwnbox/start", json_data={"location": location})
    
    def get_pwnbox_status(self) -> Dict[str, Any]:
        """Get PwnBox status"""
        return self.api.get("/pwnbox/status")
    
    def terminate_pwnbox(self) -> Dict[str, Any]:
        """Terminate a PwnBox instance"""
        return self.api.post("/pwnbox/terminate")
    
    def get_pwnbox_usage(self) -> Dict[str, Any]:
        """Get PwnBox usage statistics"""
        return self.api.get("/pwnbox/usage")

# Click commands
@click.group()
def pwnbox():
    """PwnBox-related commands"""
    pass

@pwnbox.command()
@click.option('--location', '-l', 
              type=click.Choice(['us-east', 'us-west', 'uk', 'ca', 'in', 'de', 'au']),
              default='us-east',
              help='PwnBox location')
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def start(location, debug, json_output):
    """Start a PwnBox instance"""
    try:
        api_client = HTBAPIClient()
        pwnbox_module = PwnBoxModule(api_client)
        result = pwnbox_module.start_pwnbox(location)
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: PwnBox Start", json_output)
            return
        
        if result and 'data' in result:
            data = result['data']
            console.print(Panel.fit(
                f"[bold green]PwnBox Started Successfully[/bold green]\n"
                f"ID: {data.get('id', 'N/A')}\n"
                f"Hostname: {data.get('hostname', 'N/A')}\n"
                f"Status: {data.get('status', 'N/A')}\n"
                f"Location: {data.get('location', 'N/A')}\n"
                f"Proxy URL: {data.get('proxy_url', 'N/A')}\n"
                f"Created: {data.get('created_at', 'N/A')}\n"
                f"Expires: {data.get('expires_at', 'N/A')}\n"
                f"Life Remaining: {data.get('life_remaining', 'N/A')} minutes",
                title="PwnBox Started"
            ))
        else:
            console.print("[yellow]Failed to start PwnBox[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@pwnbox.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def status(debug, json_output):
    """Get PwnBox status"""
    try:
        api_client = HTBAPIClient()
        pwnbox_module = PwnBoxModule(api_client)
        result = pwnbox_module.get_pwnbox_status()
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: PwnBox Status", json_output)
            return
        
        if result and 'data' in result:
            data = result['data']
            console.print(Panel.fit(
                f"[bold green]PwnBox Status[/bold green]\n"
                f"ID: {data.get('id', 'N/A')}\n"
                f"Hostname: {data.get('hostname', 'N/A')}\n"
                f"Status: {data.get('status', 'N/A')}\n"
                f"Location: {data.get('location', 'N/A')}\n"
                f"Proxy URL: {data.get('proxy_url', 'N/A')}\n"
                f"Username: {data.get('username', 'N/A')}\n"
                f"VNC Password: {data.get('vnc_password', 'N/A')}\n"
                f"VNC View Only Password: {data.get('vnc_view_only_password', 'N/A')}\n"
                f"Spectate URL: {data.get('spectate_url', 'N/A')}\n"
                f"Created: {data.get('created_at', 'N/A')}\n"
                f"Expires: {data.get('expires_at', 'N/A')}\n"
                f"Life Remaining: {data.get('life_remaining', 'N/A')} minutes\n"
                f"Is Ready: {data.get('is_ready', 'N/A')}",
                title="PwnBox Status"
            ))
        elif result and 'message' in result:
            console.print(Panel.fit(
                f"[yellow]PwnBox Status[/yellow]\n"
                f"Message: {result['message']}",
                title="PwnBox Status"
            ))
        else:
            console.print("[yellow]No PwnBox status found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@pwnbox.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def terminate(debug, json_output):
    """Terminate a PwnBox instance"""
    try:
        api_client = HTBAPIClient()
        pwnbox_module = PwnBoxModule(api_client)
        result = pwnbox_module.terminate_pwnbox()
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: PwnBox Terminate", json_output)
            return
        
        console.print(Panel.fit(
            "[bold green]PwnBox terminated successfully[/bold green]",
            title="PwnBox Terminated"
        ))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@pwnbox.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
@click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
def usage(debug, json_output):
    """Get PwnBox usage statistics"""
    try:
        api_client = HTBAPIClient()
        pwnbox_module = PwnBoxModule(api_client)
        result = pwnbox_module.get_pwnbox_usage()
        
        if debug or json_output:
            handle_debug_option(debug, result, "Debug: PwnBox Usage", json_output)
            return
        
        if result:
            console.print(Panel.fit(
                f"[bold green]PwnBox Usage Statistics[/bold green]\n"
                f"Total Minutes: {result.get('total', 'N/A')}\n"
                f"Used Minutes: {result.get('used', 'N/A')}\n"
                f"Remaining Minutes: {result.get('remaining', 'N/A')}\n"
                f"Active Minutes: {result.get('active_minutes', 'N/A')}\n"
                f"Allowed: {result.get('allowed', 'N/A')}\n"
                f"Sessions: {result.get('sessions', 'N/A')}",
                title="PwnBox Usage"
            ))
        else:
            console.print("[yellow]No usage statistics found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
