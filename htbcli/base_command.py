"""
Base command class for HTB CLI that automatically includes debug functionality
"""

import functools
from typing import Dict, Any, Optional, Callable
from rich.console import Console
from rich.panel import Panel
import click

console = Console()

def debug_response(result: Dict[str, Any], title: str = "Debug: API Response") -> None:
    """
    Generic debug handler to display raw API responses
    
    Args:
        result: The API response data to display
        title: The title for the debug panel
    """
    console.print(Panel.fit(
        f"[bold green]Raw API Response[/bold green]\n"
        f"{result}",
        title=title
    ))

def handle_debug_option(debug: bool, result: Dict[str, Any], title: str = "Debug: API Response") -> bool:
    """
    Generic debug option handler that can be used in any command
    
    Args:
        debug: Boolean flag indicating if debug mode is enabled
        result: The API response data to display
        title: The title for the debug panel
        
    Returns:
        bool: True if debug was handled (should return early), False otherwise
    """
    if debug:
        debug_response(result, title)
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
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract debug flag
        debug = kwargs.pop('debug', False)
        
        # Call the original function with debug flag
        return func(*args, debug=debug, **kwargs)
    
    return wrapper

def api_command(func: Callable) -> Callable:
    """
    Decorator for API commands that automatically handles debug output
    
    This decorator is specifically designed for commands that make API calls
    and want to show the raw response when --debug is used.
    
    Usage:
        @machines.command()
        @api_command
        def some_command(debug=False):
            result = api_call()
            if handle_debug_option(debug, result, "Debug: Some Command"):
                return
            # Rest of command logic
    """
    @click.option('--debug', is_flag=True, help='Show raw API response for debugging')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract debug flag
        debug = kwargs.pop('debug', False)
        
        # Call the original function with debug flag
        return func(*args, debug=debug, **kwargs)
    
    return wrapper
