# HTB CLI

A comprehensive command-line interface for the HackTheBox API, providing easy access to all HTB endpoints organized by modules.

## Features

- **Modular Design**: Organized by API categories (Machines, Challenges, Users, Seasons, Sherlocks, etc.)
- **Rich Output**: Beautiful tables and panels using Rich library
- **Easy Setup**: Simple configuration with environment variables
- **Comprehensive Coverage**: Supports all major HTB API endpoints
- **Interactive**: User-friendly command-line interface
- **Auto-completion**: Full shell completion support for bash and zsh (similar to Netexec)

## Installation

### Prerequisites

- Python 3.8 or higher
- HTB API token (get it from https://app.hackthebox.com)

### Install from source

```bash
# Clone the repository
git clone <repository-url>
cd htbcli

# Install using uv (recommended)
uv tool install .

# Or run directly without installation
uv run htbcli --help
```

## Configuration

### 1. Get your API Token

1. Go to https://app.hackthebox.com
2. Navigate to your profile settings
3. Generate an API token

### 2. Set the API Token

**Option 1: Environment Variable**
```bash
export HTB_TOKEN="your_token_here"
```

**Option 2: .env file**
Create a `.env` file in the project root:
```
HTB_TOKEN=your_token_here
```

### 3. Verify Configuration

```bash
htbcli info
```

## Auto-completion Setup

HTB CLI includes comprehensive auto-completion support for bash and zsh, similar to Netexec. This provides intelligent command and option suggestions as you type.

### Quick Setup

```bash
# Run the auto-completion installer
./install_completion.sh

# Or manually generate and source completion
source <(htbcli completion --shell bash --raw)  # For bash
source <(htbcli completion --shell zsh --raw)   # For zsh
```

### Manual Setup

1. **Generate completion script:**
   ```bash
   htbcli completion --shell bash  # For bash (shows formatted output)
   htbcli completion --shell zsh   # For zsh (shows formatted output)
   htbcli completion --shell bash --raw  # For bash (raw output for sourcing)
   htbcli completion --shell zsh --raw   # For zsh (raw output for sourcing)
   ```

2. **Add to your shell config:**
   - For bash: Add the output to `~/.bashrc`
   - For zsh: Add the output to `~/.zshrc`

3. **Reload your shell:**
   ```bash
   source ~/.bashrc  # For bash
   source ~/.zshrc   # For zsh
   ```

### Usage Examples

Once installed, you can use TAB completion:

```bash
# Complete main commands
htbcli [TAB]                    # Shows: machines, challenges, user, season, etc.

# Complete subcommands
htbcli machines [TAB]           # Shows: list, active, info, submit, etc.
htbcli challenges [TAB]         # Shows: list-challenges, info, submit, etc.

# Complete options
htbcli machines list --[TAB]    # Shows: --help, --debug, --json, etc.
htbcli machines list --difficulty [TAB]  # Shows: very-easy, easy, medium, hard, insane

# Complete choice options
htbcli machines list --os [TAB] # Shows: linux, windows, freebsd, openbsd, other
```

### Features

- **Command completion**: All main commands and subcommands
- **Option completion**: All available flags and options
- **Choice completion**: Predefined choices for options like difficulty, OS, etc.
- **Context-aware**: Suggestions change based on current command context
- **Descriptive**: Zsh completion includes descriptions for commands

## Usage

### Basic Commands

```bash
# Show help
htbcli --help
# or
uv run htbcli --help

# Show version
htbcli --version
# or
uv run htbcli --version

# Show configuration info
htbcli info
# or
uv run htbcli info

# Setup instructions
htbcli setup
# or
uv run htbcli setup

# List all available endpoints
htbcli endpoints
# or
uv run htbcli endpoints

# Show module information
htbcli module-info Machines
# or
uv run htbcli module-info Machines
```

### Machines Module

```bash
# Get currently active machine
htbcli machines active
# or
uv run htbcli machines active

# List machines (paginated)
htbcli machines list --page 1 --per-page 20 --status active
# or
uv run htbcli machines list --page 1 --per-page 20 --status active

# Get machine profile by slug
htbcli machines profile machine-name
# or
uv run htbcli machines profile machine-name

# Submit flag for machine (using active machine, machine ID, name, or stdin)
echo "flag{your_flag_here}" | htbcli machines submit
htbcli machines submit "flag{your_flag_here}"
htbcli machines submit 12345 "flag{your_flag_here}"
htbcli machines submit "machine-name" "flag{your_flag_here}"
echo "flag{your_flag_here}" | htbcli machines submit "machine-name"
```

### Challenges Module

```bash
# List challenges
htbcli challenges list --page 1 --per-page 20 --difficulty Easy
# or
uv run htbcli challenges list --page 1 --per-page 20 --difficulty Easy

# Get challenge profile
htbcli challenges profile challenge-name
# or
uv run htbcli challenges profile challenge-name

# Submit challenge flag
htbcli challenges submit "flag{your_flag_here}"
# or
uv run htbcli challenges submit "flag{your_flag_here}"
```

### User Module

```bash
# Get user profile
htbcli user profile 12345
# or
uv run htbcli user profile 12345

# Get user owns
htbcli user owns 12345
# or
uv run htbcli user owns 12345

# Get user activity
htbcli user activity 12345
# or
uv run htbcli user activity 12345

# Get user rankings
htbcli user rankings 12345
# or
uv run htbcli user rankings 12345
```

### Season Module

```bash
# List all seasons
htbcli season list
# or
uv run htbcli season list

# Get season machines
htbcli season machines
# or
uv run htbcli season machines

# Get completed season machines
htbcli season completed 1
# or
uv run htbcli season completed 1

# Submit seasonal flag
htbcli season submit "flag{your_flag_here}"
# or
uv run htbcli season submit "flag{your_flag_here}"

# Get arena stats
htbcli season stats
# or
uv run htbcli season stats
```

### Sherlocks Module

```bash
# List sherlocks
htbcli sherlocks list-sherlocks --page 1 --per-page 20
# or
uv run htbcli sherlocks list-sherlocks --page 1 --per-page 20

# List sherlocks with filtering
htbcli sherlocks list-sherlocks --difficulty easy --state active --sort-by rating
# or
uv run htbcli sherlocks list-sherlocks --difficulty easy --state active --sort-by rating

# Get sherlock categories
htbcli sherlocks categories
# or
uv run htbcli sherlocks categories

# Get sherlock info by ID or name
htbcli sherlocks info 123
htbcli sherlocks info "brutus"
# or
uv run htbcli sherlocks info 123
uv run htbcli sherlocks info "brutus"

# Download sherlock file (default behavior)
htbcli sherlocks download 123
htbcli sherlocks download "brutus"
# or
uv run htbcli sherlocks download 123
uv run htbcli sherlocks download "brutus"

# Show download link only
htbcli sherlocks download 123 --link-only
htbcli sherlocks download "brutus" --link-only
# or
uv run htbcli sherlocks download 123 --link-only
uv run htbcli sherlocks download "brutus" --link-only

# Download sherlock file with custom filename
htbcli sherlocks download 123 --output my_sherlock.zip
htbcli sherlocks download "brutus" --output brutus.zip
# or
uv run htbcli sherlocks download 123 --output my_sherlock.zip
uv run htbcli sherlocks download "brutus" --output brutus.zip

# Start playing a sherlock
htbcli sherlocks play 123
htbcli sherlocks play "brutus"
# or
uv run htbcli sherlocks play 123
uv run htbcli sherlocks play "brutus"

# Get sherlock progress
htbcli sherlocks progress 123
htbcli sherlocks progress "brutus"
# or
uv run htbcli sherlocks progress 123
uv run htbcli sherlocks progress "brutus"

# Get sherlock tasks
htbcli sherlocks tasks 123
htbcli sherlocks tasks "brutus"
# or
uv run htbcli sherlocks tasks 123
uv run htbcli sherlocks tasks "brutus"

# Submit flag for a specific sherlock task
htbcli sherlocks submit-flag 123 456 "flag{your_flag_here}"
htbcli sherlocks submit-flag "brutus" 456 "flag{your_flag_here}"
# or
uv run htbcli sherlocks submit-flag 123 456 "flag{your_flag_here}"
uv run htbcli sherlocks submit-flag "brutus" 456 "flag{your_flag_here}"

# Get sherlock writeup
htbcli sherlocks writeup 123
htbcli sherlocks writeup "brutus"
# or
uv run htbcli sherlocks writeup 123
uv run htbcli sherlocks writeup "brutus"

# Get official sherlock writeup
htbcli sherlocks writeup-official 123
htbcli sherlocks writeup-official "brutus"
# or
uv run htbcli sherlocks writeup-official 123
uv run htbcli sherlocks writeup-official "brutus"
```

### Advanced Filtering Examples

The CLI supports powerful filtering and sorting options for listing machines and challenges:

#### Machine Filtering

```bash
# Filter machines by difficulty, sort by rating (ascending), show only retired machines
htbcli machines list-machines --difficulty easy --sort-type asc --sort-by rating --status retired --show-completed incomplete

# Filter by multiple criteria
htbcli machines list-machines --difficulty medium --os linux --status active --sort-by difficulty --sort-type desc

# Show only machines you haven't completed
htbcli machines list-machines --show-completed incomplete --status active

# Filter by OS and difficulty
htbcli machines list-machines --os windows --difficulty hard --status retired

# Sort by different criteria
htbcli machines list-machines --sort-by name --sort-type asc --status active
htbcli machines list-machines --sort-by rating --sort-type desc --difficulty easy
```

#### Challenge Filtering

```bash
# Filter challenges by category, difficulty, and completion status
htbcli challenges list-challenges --state active --difficulty medium --status incompleted --category web

# Filter by multiple categories
htbcli challenges list-challenges --category web --category crypto --difficulty easy

# Show only challenges you haven't solved
htbcli challenges list-challenges --status incompleted --difficulty hard

# Filter by state and difficulty
htbcli challenges list-challenges --state active --difficulty medium --sort-by rating --sort-type desc

# Show challenges by specific category
htbcli challenges list-challenges --category pwn --difficulty medium --status incompleted
```

#### Sherlock Filtering

```bash
# Filter sherlocks by difficulty and state
htbcli sherlocks list-sherlocks --difficulty easy --state active --sort-by rating --sort-type desc

# Filter by multiple difficulties
htbcli sherlocks list-sherlocks --difficulty easy --difficulty medium --state active

# Filter by category (use category IDs from categories command)
htbcli sherlocks list-sherlocks --category 1 --category 2 --difficulty medium

# Show only completed sherlocks
htbcli sherlocks list-sherlocks --status completed --sort-by solves --sort-type desc

# Search by keyword
htbcli sherlocks list-sherlocks --keyword "web" --difficulty medium --state active

# Show only todo items
htbcli sherlocks list-sherlocks --todo --difficulty easy

# Complex filtering with multiple criteria
htbcli sherlocks list-sherlocks --difficulty medium --state active --status incompleted --sort-by rating --sort-type desc
```

#### Available Filter Options

**For Machines:**
- `--difficulty`: easy, medium, hard, insane
- `--os`: linux, windows, openbsd, solaris, freebsd, other
- `--status`: active, retired, all
- `--show-completed`: completed, incomplete, all
- `--sort-by`: name, difficulty, rating, release_date, user_rating
- `--sort-type`: asc, desc

**For Challenges:**
- `--difficulty`: easy, medium, hard, insane
- `--category`: web, crypto, pwn, forensics, reverse, stego, osint, mobile, hardware, misc
- `--state`: active, retired, all
- `--status`: completed, incompleted, all
- `--sort-by`: name, difficulty, rating, release_date, solves
- `--sort-type`: asc, desc

**For Sherlocks:**
- `--difficulty`: very-easy, easy, medium, hard, insane
- `--state`: active, retired, unreleased
- `--category`: category ID (use `htbcli sherlocks categories` to see available IDs)
- `--status`: completed, incompleted
- `--sort-by`: solves, category, rating, name
- `--sort-type`: asc, desc
- `--keyword`: search by keyword
- `--todo`: show only todo items
```

## Available Modules

The CLI is organized into the following modules based on the HTB API:

- **Machines**: Machine-related endpoints (active, list, profile, submit flags)
- **Challenges**: Challenge-related endpoints (list, profile, submit flags)
- **User**: User profile and statistics endpoints
- **Season**: Season/Arena-related endpoints
- **Sherlocks**: Sherlock-related endpoints (list, categories, info, download, play, progress, tasks, submit flags, writeups)
- **Badges**: Badge-related endpoints
- **Career**: Career-related endpoints (companies, jobs, applications)
- **Connection**: VPN connection endpoints (servers, status, connect/disconnect)
- **Fortresses**: Fortress-related endpoints (list, profile, submit flags)
- **Home**: Home page banner endpoints (banners, announcements, dashboard, news)
- **Platform**: General platform endpoints (announcements, dashboard, notifications, stats, status, health)
- **Prolabs**: ProLab-related endpoints (list, profile, machines, submit flags)
- **PwnBox**: PwnBox-related endpoints (status, info, config, logs)
- **Ranking**: Ranking endpoints (global, country, machine, challenge, user rankings)
- **Review**: Product review endpoints (list reviews, get review details)
- **Starting Point**: Starting Point endpoints (list, profile, submit flags)
- **Team**: Team ranking endpoints (list teams, profiles, members, rankings, stats)
- **Tracks**: Track-related endpoints (list, profile, progress, modules)
- **Universities**: University ranking endpoints (list, profile, rankings, stats)
- **VM**: VM spawning operations (spawn, extend, reset, terminate, vote reset, accept reset vote)

## Examples

### Get Active Machine Information
```bash
htbcli machines active
# or
uv run htbcli machines active
```

### List First Page of Active Machines
```bash
htbcli machines list --page 1 --per-page 10 --status active
# or
uv run htbcli machines list --page 1 --per-page 10 --status active
```

### Submit a Flag
```bash
# Submit flag to active machine (most convenient)
echo "flag{abc123def456}" | htbcli machines submit
htbcli machines submit "flag{abc123def456}"

# Submit flag using machine ID
htbcli machines submit 12345 "flag{abc123def456}"

# Submit flag using machine name
htbcli machines submit "machine-name" "flag{abc123def456}"

# Submit flag piped from stdin to specific machine
echo "flag{abc123def456}" | htbcli machines submit "machine-name"

# Submit flag from environment variable to active machine
echo $FLAG | htbcli machines submit
```

### Get User Profile
```bash
htbcli user profile 12345
# or
uv run htbcli user profile 12345
```

### VM Operations
```bash
# Spawn a VM for machine ID 123
htbcli vm spawn 123
# or
uv run htbcli vm spawn 123

# Extend VM time for machine ID 123
htbcli vm extend 123
# or
uv run htbcli vm extend 123

# Reset VM for machine ID 123
htbcli vm reset 123
# or
uv run htbcli vm reset 123

# Terminate VM for machine ID 123
htbcli vm terminate 123
# or
uv run htbcli vm terminate 123

# Vote to reset VM for machine ID 123
htbcli vm vote-reset 123
# or
uv run htbcli vm vote-reset 123

# Accept reset vote for machine ID 123
htbcli vm accept-vote 123
# or
uv run htbcli vm accept-vote 123
```

### VPN Management
```bash
# List available VPN servers
htbcli vpn list
# or
uv run htbcli vpn list

# Download all VPN configurations
htbcli vpn download
# or
uv run htbcli vpn download

# List downloaded VPN files
htbcli vpn files
# or
uv run htbcli vpn files

# Start VPN connection (requires sudo)
htbcli vpn start "EU VIP 7" --mode udp
# or
uv run htbcli vpn start "EU VIP 7" --mode udp

# Stop VPN connection
htbcli vpn stop
# or
uv run htbcli vpn stop

# Get VPN connection status
htbcli vpn status
# or
uv run htbcli vpn status
```

**Note**: VPN operations require OpenVPN to be installed and may require sudo privileges.

### Get VM Status
```bash
# Get active machine and VM status
htbcli machines active
# or
uv run htbcli machines active

# Get VM status (alias)
htbcli machines vm-status
# or
uv run htbcli machines vm-status
```

### List All Available Endpoints
```bash
htbcli endpoints
# or
uv run htbcli endpoints
```

## Error Handling

The CLI provides clear error messages for common issues:

- **Missing API Token**: Set the `HTB_TOKEN` environment variable
- **Invalid Endpoint**: Check the endpoint name and parameters
- **Network Issues**: Verify your internet connection
- **API Errors**: Check the API response for specific error details

## Development

### Project Structure

```
htbcli/
├── htbcli/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── config.py           # Configuration management
│   ├── api_client.py       # API client
│   ├── swagger_parser.py   # OpenAPI parser
│   └── modules/            # API modules
│       ├── __init__.py
│       ├── machines.py
│       ├── challenges.py
│       ├── user.py
│       ├── season.py
│       └── sherlocks.py
├── requirements.txt
├── setup.py
├── README.md
└── swagger.htb             # HTB API specification
```

### Adding New Modules

1. Create a new module file in `htbcli/modules/`
2. Define the module class with API methods
3. Create Click commands for the module
4. Add the module to `htbcli/modules/__init__.py`
5. Import and add the module to `htbcli/cli.py`

### Running Tests

```bash
# Install test dependencies
uv add pytest

# Run tests
uv run pytest
# or
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is not affiliated with or endorsed by HackTheBox. It's a community-maintained tool for interacting with the HTB API.

## Support

If you encounter any issues or have questions:

1. Check the error messages for guidance
2. Verify your API token is correct
3. Ensure you have the latest version
4. Open an issue on GitHub with details about the problem

## Changelog

### v1.0.0
- Initial release
- Support for Machines, Challenges, Users, Seasons, and Sherlocks modules
- Rich CLI interface with tables and panels
- Comprehensive error handling
- Easy configuration setup
