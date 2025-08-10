# HTB CLI

A comprehensive command-line interface for the HackTheBox API, providing easy access to all HTB endpoints organized by modules.

## Features

- **Modular Design**: Organized by API categories (Machines, Challenges, Users, Seasons, Sherlocks, etc.)
- **Rich Output**: Beautiful tables and panels using Rich library
- **Easy Setup**: Simple configuration with environment variables
- **Comprehensive Coverage**: Supports all major HTB API endpoints
- **Interactive**: User-friendly command-line interface

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
uv pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
pip install -e .
```

### Install dependencies only

```bash
pip install requests click pyyaml rich tabulate python-dotenv
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
# If using uv
.venv/bin/htbcli info

# Or if installed globally
htbcli info
```

## Usage

### Basic Commands

```bash
# Show help
.venv/bin/htbcli --help

# Show version
.venv/bin/htbcli --version

# Show configuration info
.venv/bin/htbcli info

# Setup instructions
.venv/bin/htbcli setup

# List all available endpoints
.venv/bin/htbcli endpoints

# Show module information
.venv/bin/htbcli module-info Machines
```

### Machines Module

```bash
# Get currently active machine
.venv/bin/htbcli machines active

# List machines (paginated)
.venv/bin/htbcli machines list --page 1 --per-page 20 --status active

# Get machine profile by slug
.venv/bin/htbcli machines profile machine-name

# Submit flag for machine
.venv/bin/htbcli machines submit "flag{your_flag_here}"
```

### Challenges Module

```bash
# List challenges
.venv/bin/htbcli challenges list --page 1 --per-page 20 --difficulty Easy

# Get challenge profile
.venv/bin/htbcli challenges profile challenge-name

# Submit challenge flag
.venv/bin/htbcli challenges submit "flag{your_flag_here}"
```

### User Module

```bash
# Get user profile
.venv/bin/htbcli user profile 12345

# Get user owns
.venv/bin/htbcli user owns 12345

# Get user activity
.venv/bin/htbcli user activity 12345

# Get user rankings
.venv/bin/htbcli user rankings 12345
```

### Season Module

```bash
# List all seasons
.venv/bin/htbcli season list

# Get season machines
.venv/bin/htbcli season machines

# Get completed season machines
.venv/bin/htbcli season completed 1

# Submit seasonal flag
.venv/bin/htbcli season submit "flag{your_flag_here}"

# Get arena stats
.venv/bin/htbcli season stats
```

### Sherlocks Module

```bash
# List sherlocks
.venv/bin/htbcli sherlocks list --page 1 --per-page 20

# Get sherlock profile
.venv/bin/htbcli sherlocks profile sherlock-name

# Submit sherlock flag
.venv/bin/htbcli sherlocks submit "flag{your_flag_here}"
```

## Available Modules

The CLI is organized into the following modules based on the HTB API:

- **Machines**: Machine-related endpoints (active, list, profile, submit flags)
- **Challenges**: Challenge-related endpoints (list, profile, submit flags)
- **User**: User profile and statistics endpoints
- **Season**: Season/Arena-related endpoints
- **Sherlocks**: Sherlock-related endpoints
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
- **VM**: VM spawning endpoints (spawn, terminate, status, info, connection, logs)

## Examples

### Get Active Machine Information
```bash
.venv/bin/htbcli machines active
```

### List First Page of Active Machines
```bash
.venv/bin/htbcli machines list --page 1 --per-page 10 --status active
```

### Submit a Flag
```bash
.venv/bin/htbcli machines submit "flag{abc123def456}"
```

### Get User Profile
```bash
.venv/bin/htbcli user profile 12345
```

### List All Available Endpoints
```bash
.venv/bin/htbcli endpoints
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
pip install pytest

# Run tests
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
