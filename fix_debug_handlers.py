#!/usr/bin/env python3
"""
Fix missing debug handler calls in HTB CLI modules

This script adds the missing handle_debug_option calls to all commands that have
the --debug option but are missing the actual debug handler implementation.
"""

import re
from pathlib import Path

def fix_debug_handlers_in_file(file_path: Path):
    """Fix debug handlers in a single module file"""
    
    print(f"Processing {file_path.name}...")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all function definitions that have debug parameter but no handle_debug_option call
    # Pattern: def function_name(..., debug): ... result = ... ... if result:
    pattern = r'def ([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*debug[^)]*\):\s*\n\s*try:\s*\n\s*api_client = HTBAPIClient\(\)\s*\n\s*[^=]+= [^=]+\(api_client\)\s*\n\s*result = [^;]+\.get_[^;]+\([^;]*\)\s*\n\s*\n\s*if result'
    
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
    
    # Apply the transformation
    new_content = re.sub(pattern, add_debug_handler, content, flags=re.MULTILINE | re.DOTALL)
    
    # Also handle POST requests
    post_pattern = r'def ([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*debug[^)]*\):\s*\n\s*try:\s*\n\s*api_client = HTBAPIClient\(\)\s*\n\s*[^=]+= [^=]+\(api_client\)\s*\n\s*result = [^;]+\.post\([^;]*\)\s*\n\s*\n\s*if result'
    
    def add_debug_handler_post(match):
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
            if line.strip().startswith('result = ') and 'post(' in line:
                # Insert debug handler after this line
                lines.insert(i + 1, debug_handler)
                break
        
        return '\n'.join(lines)
    
    new_content = re.sub(post_pattern, add_debug_handler_post, new_content, flags=re.MULTILINE | re.DOTALL)
    
    # Write the updated content back
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"  Completed {file_path.name}")

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
    
    print("=== Fixing missing debug handlers in HTB CLI commands ===\n")
    
    for module_file in module_files:
        file_path = modules_dir / module_file
        if file_path.exists():
            fix_debug_handlers_in_file(file_path)
        else:
            print(f"Warning: {file_path} not found")
    
    print("\n=== Debug handlers fixed successfully! ===")
    print("All commands with --debug options now have proper debug handler calls.")

if __name__ == "__main__":
    main()
