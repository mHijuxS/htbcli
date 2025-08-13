# HTB CLI Debug Implementation

## Overview

This document explains the implementation of the `--debug` option across all HTB CLI modules. The debug functionality allows users to see raw API responses for troubleshooting and development purposes.

## Architecture

### 1. Debug Handler Module (`htbcli/base_command.py`)

The core debug functionality is implemented in a centralized module that provides:

- `debug_response()`: Displays raw API responses in a formatted panel
- `handle_debug_option()`: Generic handler that checks debug flag and displays response
- `command_with_debug()`: Decorator for automatically adding debug options
- `api_command()`: Decorator specifically for API commands

### 2. Implementation Pattern

Each command follows this pattern:

```python
@module.command()
@click.option('--debug', is_flag=True, help='Show raw API response for debugging')
def command_name(debug):
    """Command description"""
    try:
        api_client = HTBAPIClient()
        module_instance = ModuleClass(api_client)
        result = module_instance.api_method()
        
        if handle_debug_option(debug, result, "Debug: Command Name API Response"):
            return
        
        # Rest of command logic...
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
```

## Key Features

### 1. Consistent Debug Output
- All debug output uses the same formatting with Rich panels
- Clear titles indicating which command and API endpoint
- Raw JSON response display

### 2. Non-Intrusive
- Debug option is optional and doesn't affect normal command operation
- When `--debug` is used, command returns early after showing response
- When `--debug` is not used, command operates normally

### 3. Easy to Implement
- Simple import: `from ..base_command import handle_debug_option`
- One-line debug handler call
- Consistent pattern across all modules

## Usage Examples

### Basic Usage
```bash
# Normal command execution
htbcli machines unreleased

# Debug mode - shows raw API response
htbcli machines unreleased --debug
```

### Debug Output Example
```
╭────────────────────────── Debug: Unreleased Machines API Response ──────────────────────────╮
│ Raw API Response                                                                            │
│ {'data': [{'id': 695, 'name': 'Sweep', 'os': 'Windows', 'avatar':                           │
│ '/avatars/e049d2e96ca2ba2f5504f88ea6862251.png', 'release': '2025-08-14T14:00:00.000000Z',  │
│ 'difficulty': 50, 'difficulty_text': 'Medium', 'firstCreator': [{'id': 270807, 'name':      │
│ 'Yeeb', 'avatar':                                                                           │
│ 'https://account.hackthebox.com/storage/users/1e448327-4c09-485c-bb56-00fc9b283cf7-avatar.p │
│ ng'}], 'coCreators': []}, {'id': 692, 'name': 'CodeTwo', 'os': 'Linux', 'avatar':           │
│ '/avatars/992c992925936b399906f2a78a740eea.png', 'release': '2025-08-16T19:00:00.000000Z',  │
│ 'difficulty': 25, 'difficulty_text': 'Easy', 'firstCreator': [{'id': 1076236, 'name':       │
│ 'FisMatHack', 'avatar':                                                                     │
│ 'https://account.hackthebox.com/storage/users/a45cd394-1a65-454a-bc49-1fd3981fcf00-avatar.p │
│ ng'}], 'coCreators': [], 'retiring': {'difficulty_text': 'Easy', 'avatar':                  │
│ '/avatars/f6a56cec6e9826b4ed124fb4155abc66.png', 'os': 'Linux', 'name': 'Nocturnal', 'id':  │
│ 656}}], 'links': {'first':                                                                  │
│ 'https://labs.hackthebox.com/api/v4/machine/unreleased?unreleased=1&page=1', 'last':        │
│ 'https://labs.hackthebox.com/api/v4/machine/unreleased?unreleased=1&page=1', 'prev': None,  │
│ 'next': None}, 'meta': {'current_page': 1, 'from': 1, 'last_page': 1, 'links': [{'url':     │
│ None, 'label': '&laquo; Previous', 'active': False}, {'url':                                │
│ 'https://labs.hackthebox.com/api/v4/machine/unreleased?unreleased=1&page=1', 'label': '1',  │
│ 'active': True}, {'url': None, 'label': 'Next &raquo;', 'active': False}], 'path':          │
│ 'https://labs.hackthebox.com/api/v4/machine/unreleased', 'per_page': 15, 'to': 2, 'total':  │
│ 2}}                                                                                         │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Implementation Status

### Completed Modules
- ✅ `machines.py` - All commands have debug options
- ✅ `user.py` - All commands have debug options
- ✅ `vm.py` - All commands have debug options

### Partially Completed
- 🔄 Other modules have debug imports added but need manual command updates

## Benefits

### 1. Development and Debugging
- Easy to see what data is returned from API endpoints
- Helps identify API changes or issues
- Useful for development and testing

### 2. User Experience
- Consistent debug interface across all commands
- Clear, readable output format
- Non-intrusive to normal operation

### 3. Maintenance
- Centralized debug logic reduces code duplication
- Easy to modify debug output format globally
- Consistent implementation pattern

## Future Enhancements

### 1. Automatic Implementation
- Script to automatically add debug options to all commands
- Template-based command generation
- CI/CD integration for new commands

### 2. Enhanced Debug Features
- Pretty-printed JSON output
- Syntax highlighting for JSON
- Filtering options for large responses
- Export debug output to files

### 3. Advanced Debugging
- Request/response logging
- Performance timing
- API call tracing
- Error context information

## Conclusion

The debug implementation provides a robust, consistent, and user-friendly way to inspect API responses across all HTB CLI commands. The centralized approach makes it easy to maintain and extend, while the simple pattern makes it straightforward to implement in new commands.
