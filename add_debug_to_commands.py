#!/usr/bin/env python3
"""
Simple utility to add debug options to HTB CLI commands

This script demonstrates the pattern for adding debug functionality to commands.
Instead of manually adding --debug to every command, you can use the debug handler.

Usage:
    python add_debug_to_commands.py

The script will show examples of how to add debug options to commands.
"""

import re
from pathlib import Path

def show_debug_pattern():
    """Show the pattern for adding debug options to commands"""
    
    print("=== HTB CLI Debug Option Pattern ===\n")
    
    print("1. Import the debug handler in your module:")
    print("   from ..base_command import handle_debug_option\n")
    
    print("2. Add --debug option to your command:")
    print("   @click.option('--debug', is_flag=True, help='Show raw API response for debugging')")
    print("   def your_command(debug):")
    print("       # ... your code ...")
    print("       result = api_call()")
    print("       if handle_debug_option(debug, result, \"Debug: Your Command API Response\"):")
    print("           return")
    print("       # ... rest of your code ...\n")
    
    print("3. Example implementation:")
    print("""
@machines.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
def unreleased(debug):
    \"\"\"Get unreleased machines\"\"\"
    try:
        api_client = HTBAPIClient()
        machines_module = MachinesModule(api_client)
        result = machines_module.get_machine_unreleased()
        
        if handle_debug_option(debug, result, "Debug: Unreleased Machines API Response"):
            return
        
        # Rest of command logic...
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
""")

def find_commands_without_debug():
    """Find commands that don't have debug options yet"""
    
    modules_dir = Path("htbcli/modules")
    commands_without_debug = []
    
    for module_file in modules_dir.glob("*.py"):
        if module_file.name == "__init__.py":
            continue
            
        module_name = module_file.stem
        content = module_file.read_text()
        
        # Find commands that don't have debug options
        command_pattern = rf'@{module_name}\.command\(\)\s*\n(?:@click\.argument\([^)]+\)\s*\n)*def ([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\):'
        
        matches = re.finditer(command_pattern, content)
        for match in matches:
            func_name = match.group(1)
            params = match.group(2)
            
            # Skip if already has debug option
            if 'debug' in params:
                continue
                
            commands_without_debug.append({
                'module': module_name,
                'command': func_name,
                'file': str(module_file)
            })
    
    return commands_without_debug

def show_commands_to_update():
    """Show which commands need debug options"""
    
    commands = find_commands_without_debug()
    
    print("=== Commands that need debug options ===\n")
    
    if not commands:
        print("All commands already have debug options!")
        return
    
    # Group by module
    modules = {}
    for cmd in commands:
        module = cmd['module']
        if module not in modules:
            modules[module] = []
        modules[module].append(cmd['command'])
    
    for module, cmds in modules.items():
        print(f"{module}:")
        for cmd in cmds:
            print(f"  - {cmd}")
        print()

def main():
    """Main function"""
    show_debug_pattern()
    show_commands_to_update()
    
    print("=== Quick Implementation Guide ===\n")
    print("To add debug to a command:")
    print("1. Add import: from ..base_command import handle_debug_option")
    print("2. Add decorator: @click.option('--debug', is_flag=True, help='Show raw API response for debugging')")
    print("3. Add parameter: def command_name(debug):")
    print("4. Add debug handler after API call:")
    print("   if handle_debug_option(debug, result, \"Debug: Command Name API Response\"):")
    print("       return")

if __name__ == "__main__":
    main()
