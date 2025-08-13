"""
Debug handler utility for HTB CLI
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

def with_debug_option(func: Callable) -> Callable:
    """
    Decorator that automatically adds --debug option to any Click command
    
    Usage:
        @machines.command()
        @with_debug_option
        def some_command():
            # Command implementation
            pass
    """
    @click.option('--debug', is_flag=True, help='Show raw API response for debugging')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract debug flag from kwargs
        debug = kwargs.pop('debug', False)
        
        # Call the original function
        result = func(*args, **kwargs)
        
        # If debug is enabled and we have a result, show it
        if debug and result is not None:
            # Try to determine a good title for the debug output
            func_name = func.__name__.replace('_', ' ').title()
            title = f"Debug: {func_name} API Response"
            debug_response(result, title)
        
        return result
    
    return wrapper

def debug_command(func: Callable) -> Callable:
    """
    Alternative decorator that modifies the command to handle debug internally
    
    This decorator automatically adds the --debug option and handles the debug logic
    within the command function.
    """
    @click.option('--debug', is_flag=True, help='Show raw API response for debugging')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract debug flag
        debug = kwargs.pop('debug', False)
        
        # Call the original function with debug flag
        return func(*args, debug=debug, **kwargs)
    
    return wrapper
