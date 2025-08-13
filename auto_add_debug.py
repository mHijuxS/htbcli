#!/usr/bin/env python3
"""
Automatically add debug options to HTB CLI commands

This script automatically adds the --debug option and debug handler to commands
that don't already have it.
"""

import re
from pathlib import Path

def add_debug_to_module(module_file: Path):
    """Add debug options to all commands in a module file"""
    
    print(f"Processing {module_file.name}...")
    
    # Read the file
    with open(module_file, 'r') as f:
        content = f.read()
    
    module_name = module_file.stem
    
    # Add debug import if not present
    if 'from ..base_command import handle_debug_option' not in content:
        import_pattern = r'(from \.\.api_client import HTBAPIClient)'
        replacement = r'\1\nfrom ..base_command import handle_debug_option'
        content = re.sub(import_pattern, replacement, content)
        print(f"  Added debug import to {module_file.name}")
    
    # Find commands that don't have debug options
    command_pattern = rf'@{module_name}\.command\(\)\s*\n(?:@click\.argument\([^)]+\)\s*\n)*def ([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\):'
    
    def add_debug_to_command(match):
        full_match = match.group(0)
        func_name = match.group(1)
        params = match.group(2)
        
        # Skip if already has debug option
        if 'debug' in params:
            return full_match
        
        # Add debug option decorator
        debug_decorator = '@click.option(\'--debug\', is_flag=True, help=\'Show raw API response for debugging\')\n'
        
        # Update function signature
        if params.strip():
            new_params = f"{params}, debug"
        else:
            new_params = "debug"
        
        # Replace the command
        new_command = full_match.replace(
            f"@{module_name}.command()",
            f"@{module_name}.command()\n{debug_decorator}"
        ).replace(
            f"def {func_name}({params}):",
            f"def {func_name}({new_params}):"
        )
        
        return new_command
    
    # Apply the transformation
    new_content = re.sub(command_pattern, add_debug_to_command, content)
    
    # Add debug handler calls after API calls
    # Pattern to match: result = module.method_call()
    api_call_pattern = rf'def ([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\):\s*\n\s*try:\s*\n\s*api_client = HTBAPIClient\(\)\s*\n\s*[^=]+= [^=]+\(api_client\)\s*\n\s*result = [^;]+\.get_[^;]+\([^;]*\)\s*\n\s*\n'
    
    def add_debug_handler(match):
        func_name = match.group(1)
        func_content = match.group(0)
        
        # Skip if already has debug handler
        if 'handle_debug_option' in func_content:
            return func_content
        
        # Add debug handler after the API call
        debug_handler = f'        if handle_debug_option(debug, result, f"Debug: {func_name.title()} API Response"):\n            return\n\n'
        
        # Find the API call line and add debug handler after it
        lines = func_content.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('result = ') and 'get_' in line:
                # Insert debug handler after this line
                lines.insert(i + 1, debug_handler)
                break
        
        return '\n'.join(lines)
    
    new_content = re.sub(api_call_pattern, add_debug_handler, new_content)
    
    # Write the updated content back
    with open(module_file, 'w') as f:
        f.write(new_content)
    
    print(f"  Completed {module_file.name}")

def main():
    """Main function to process all module files"""
    
    modules_dir = Path("htbcli/modules")
    
    # List of module files to process
    module_files = [
        "machines.py",
        "user.py", 
        "challenges.py",
        "season.py",
        "vpn.py",
        "platform.py",
        "team.py",
        "universities.py",
        "fortresses.py",
        "prolabs.py",
        "pwnbox.py",
        "ranking.py",
        "starting_point.py",
        "tracks.py",
        "badges.py",
        "career.py",
        "home.py",
        "review.py",
        "sherlocks.py",
        "connection.py"
    ]
    
    print("=== Auto-adding debug options to HTB CLI commands ===\n")
    
    for module_file in module_files:
        file_path = modules_dir / module_file
        if file_path.exists():
            add_debug_to_module(file_path)
        else:
            print(f"Warning: {file_path} not found")
    
    print("\n=== Debug options added successfully! ===")
    print("You can now use --debug with any command to see raw API responses.")

if __name__ == "__main__":
    main()
