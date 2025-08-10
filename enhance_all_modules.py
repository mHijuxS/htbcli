#!/usr/bin/env python3
"""
Script to enhance all HTB CLI modules with comprehensive response handling
"""

import os
import re
from pathlib import Path

def enhance_module_file(file_path):
    """Enhance a single module file with response options"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match Click commands that don't have response options yet
    command_pattern = r'@(\w+)\.command\(\)\s*\n(?!.*@click\.option.*responses)'
    
    def add_response_options(match):
        command_name = match.group(1)
        return f'@{command_name}.command()\n@click.option(\'--responses\', is_flag=True, help=\'Show all available response fields\')\n@click.option(\'-o\', \'--option\', multiple=True, help=\'Show specific field(s) (can be used multiple times)\')'
    
    # Add response options to commands
    content = re.sub(command_pattern, add_response_options, content)
    
    # Pattern to match function definitions that need response parameters
    func_pattern = r'def (\w+)\(([^)]*)\):'
    
    def add_response_params(match):
        func_name = match.group(1)
        params = match.group(2)
        
        # Skip if already has responses parameter
        if 'responses' in params:
            return match.group(0)
        
        # Add responses and option parameters
        if params.strip():
            new_params = f"{params}, responses, option"
        else:
            new_params = "responses, option"
        
        return f'def {func_name}({new_params}):'
    
    content = re.sub(func_pattern, add_response_params, content)
    
    # Pattern to match result handling blocks that need enhancement
    result_pattern = r'if result and (\'data\' in result|\'info\' in result):'
    
    def enhance_result_handling(match):
        condition = match.group(1)
        return f'''if result and {condition}:
            data = result.get('data') or result.get('info') or result
            
            if responses:
                # Show all available fields
                if isinstance(data, list) and data:
                    first_item = data[0]
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields[/bold green]\\n"
                        f"{{chr(10).join([f'{{k}}: {{v}}' for k, v in first_item.items()])}}",
                        title="All Fields (First Item)"
                    ))
                elif isinstance(data, dict):
                    console.print(Panel.fit(
                        f"[bold green]All Available Fields[/bold green]\\n"
                        f"{{chr(10).join([f'{{k}}: {{v}}' for k, v in data.items()])}}",
                        title="All Fields"
                    ))
            elif option:
                # Show only specified fields
                if isinstance(data, list):
                    table = Table(title="Selected Fields")
                    table.add_column("ID", style="cyan")
                    for field in option:
                        table.add_column(field.title(), style="green")
                    
                    for item in data:
                        row = [str(item.get('id', 'N/A') or 'N/A')]
                        for field in option:
                            row.append(str(item.get(field, 'N/A') or 'N/A'))
                        table.add_row(*row)
                    
                    console.print(table)
                elif isinstance(data, dict):
                    selected_data = {{}}
                    for field in option:
                        if field in data:
                            selected_data[field] = data[field]
                        else:
                            console.print(f"[yellow]Field '{{field}}' not found in response[/yellow]")
                    
                    if selected_data:
                        console.print(Panel.fit(
                            f"[bold green]Selected Fields[/bold green]\\n"
                            f"{{chr(10).join([f'{{k}}: {{v}}' for k, v in selected_data.items()])}}",
                            title="Selected Fields"
                        ))
            else:'''
    
    content = re.sub(result_pattern, enhance_result_handling, content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Enhanced {file_path}")

def main():
    """Main function to enhance all modules"""
    
    modules_dir = Path("htbcli/modules")
    
    # List of modules to enhance (excluding __init__.py)
    module_files = [
        "badges.py",
        "career.py", 
        "connection.py",
        "fortresses.py",
        "home.py",
        "prolabs.py",
        "pwnbox.py",
        "ranking.py",
        "review.py",
        "season.py",
        "sherlocks.py",
        "starting_point.py",
        "tracks.py",
        "universities.py",
        "vm.py"
    ]
    
    for module_file in module_files:
        file_path = modules_dir / module_file
        if file_path.exists():
            try:
                enhance_module_file(file_path)
            except Exception as e:
                print(f"Error enhancing {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()
