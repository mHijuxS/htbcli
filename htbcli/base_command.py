"""
Base command class for HTB CLI that automatically includes debug functionality
"""

import functools
import json
from typing import Dict, Any, Optional, Callable
from rich.console import Console
from rich.panel import Panel
import click

console = Console()

def debug_response(result: Dict[str, Any], title: str = "Debug: API Response", json_output: bool = False) -> None:
    """
    Generic debug handler to display raw API responses
    
    Args:
        result: The API response data to display
        title: The title for the debug panel
        json_output: If True, output as JSON for jq parsing. If False, use Rich formatting.
    """
    if json_output:
        # Output as proper JSON for jq parsing
        print(json.dumps(result, indent=2, default=str))
    else:
        # Use Rich formatting for human-readable display
        console.print(Panel.fit(
            f"[bold green]Raw API Response[/bold green]\n"
            f"{result}",
            title=title
        ))

def handle_debug_option(debug: bool, result: Dict[str, Any], title: str = "Debug: API Response", json_output: bool = False) -> bool:
    """
    Generic debug option handler that can be used in any command
    
    Args:
        debug: Boolean flag indicating if debug mode is enabled
        result: The API response data to display
        title: The title for the debug panel
        json_output: If True, output as JSON for jq parsing. If False, use Rich formatting.
        
    Returns:
        bool: True if debug was handled (should return early), False otherwise
    """
    if debug or json_output:
        debug_response(result, title, json_output)
        return True
    return False

def command_with_debug(func: Callable) -> Callable:
    """
    Decorator that automatically adds --debug option to any Click command
    and handles the debug logic internally.
    
    This decorator should be used instead of @click.command() to automatically
    include debug functionality.
    
    Usage:
        @command_with_debug
        def some_command():
            # Command implementation
            pass
    """
    @click.option('--debug', is_flag=True, help='Show raw API response for debugging')
    @click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract debug flags
        debug = kwargs.pop('debug', False)
        json_output = kwargs.pop('json_output', False)
        
        # Call the original function with debug flags
        return func(*args, debug=debug, json_output=json_output, **kwargs)
    
    return wrapper

def api_command(func: Callable) -> Callable:
    """
    Decorator for API commands that automatically handles debug output
    
    This decorator is specifically designed for commands that make API calls
    and want to show the raw response when --debug is used.
    
    Usage:
        @machines.command()
        @api_command
        def some_command(debug=False, json_output=False):
            result = api_call()
            if handle_debug_option(debug, result, "Debug: Some Command", json_output):
                return
            # Rest of command logic
    """
    @click.option('--debug', is_flag=True, help='Show raw API response for debugging')
    @click.option('--json', 'json_output', is_flag=True, help='Output debug info as JSON for jq parsing')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract debug flags
        debug = kwargs.pop('debug', False)
        json_output = kwargs.pop('json_output', False)
        
        # Call the original function with debug flags
        return func(*args, debug=debug, json_output=json_output, **kwargs)
    
    return wrapper
