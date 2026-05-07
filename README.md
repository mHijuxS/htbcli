# HTB CLI

A comprehensive command-line interface for the HackTheBox API (v4 and v5),
providing easy access to machines, challenges, sherlocks, fortresses, prolabs,
seasons, VPN configs, VM operations, and more — all organized into modules.

## Features

- **Modular Design**: Organized by API categories (Machines, Challenges, Users, Seasons, Sherlocks, Fortresses, ProLabs, VM, VPN, etc.)
- **Rich Output**: Tables and panels rendered with the Rich library
- **Flexible Filtering**: Powerful list/sort/filter options for machines, challenges and sherlocks
- **Flag Submission**: Supports flag arguments, stdin piping and active-machine auto-detection
- **VPN Management**: List, switch, download and start/stop OpenVPN configs from the CLI
- **VM Lifecycle**: Spawn, wait, reset, terminate, vote-reset and accept-reset for HTB VMs
- **Debug Mode**: `--debug` and `--json` flags expose the raw API response (useful with `jq`)
- **Field Selection**: `--responses` lists every field returned by an endpoint, `-o/--option` selects specific ones
- **Suspicious Activity Analysis**: Heuristic profile auditing (`htbcli suspicious`)
- **Shell Completion**: Bash and zsh completion scripts

## Installation

### Prerequisites

- Python 3.8.1 or higher
- An HTB API token (App Token) from https://app.hackthebox.com/profile/settings

### Install with uv (recommended)

```bash
# Clone the repository
git clone <repository-url>
cd htbcli

# Install as a uv tool (puts `htbcli` on your PATH)
uv tool install .

# Or run directly from the repo without installing
uv run htbcli --help
```

### Install with pip

```bash
pip install .
```

## Authentication

HTB CLI authenticates using a single environment variable: `HTB_TOKEN`. It is
resolved from the first source that provides a value, in this order:

1. The shell environment (`export HTB_TOKEN=...`)
2. `./.env` in the current working directory
3. `~/.htbcli/.env` (works anywhere, including when `htbcli` is installed globally)
4. The path in `HTBCLI_ENV_FILE` if that variable is set (explicit override)

### Recommended: put your token in `~/.htbcli/.env`

This works whether you launch `htbcli` from the repo, from `~`, from `/tmp`, or
from anywhere else — nothing has to be on `PATH` except `htbcli`.

```bash
uv run htbcli setup      # creates ~/.htbcli and prints the .env path
mkdir -p ~/.htbcli
echo 'HTB_TOKEN=your_app_token_here' > ~/.htbcli/.env
chmod 600 ~/.htbcli/.env
```

### Alternative: shell environment variable

```bash
export HTB_TOKEN="your_app_token_here"
# add to ~/.bashrc / ~/.zshrc to make it persistent
```

A shell-level `HTB_TOKEN` always wins over any `.env` file, so you can use a
shell variable to temporarily override an `.env`-based default.

### Verify your configuration

```bash
uv run htbcli info
```

You should see `API Token: Set`. If it shows `Not Set`, none of the sources
above supplied a token.

## Usage

### Top-level commands

```bash
uv run htbcli --help        # show all commands
uv run htbcli --version     # show version
uv run htbcli info          # show config + token status
uv run htbcli setup         # print setup instructions
uv run htbcli endpoints     # list API modules from the bundled OpenAPI spec
uv run htbcli module-info Machines   # detailed endpoints for a module
uv run htbcli completion --shell zsh # generate shell completion script
```

### Available command groups

| Group | Description |
|---|---|
| `machines` | Machine list/profile/info/search, VM tasks, walkthroughs, flag submission |
| `challenges` | Challenge list/info/download, start/stop, todo list, flag submission |
| `sherlocks` | Sherlock list/info/download, play/progress/tasks, flag submission |
| `fortresses` | Fortress list/info, flags, vote reset, flag submission |
| `prolabs` | ProLab list/info, machines, flags, reviews, subscription |
| `starting-point` | Starting Point list/info, activity, writeups |
| `tracks` | Track list/info, items, writeup |
| `season` | Season list, machines, leaderboard, rewards, user rank |
| `user` | User profile/info/activity/bloods/badges/dashboard, follow/respect, etc. |
| `team` | Team list/info, activity, recommended, writeups |
| `universities` | University list, profile, members, rankings, stats |
| `ranking` | Generic ranking list/info, recommended, writeups |
| `badges` | Badge list |
| `career` | Careers list/info, activity, recommended, writeups |
| `home` | Home page banners, recommended content, user progress/todo |
| `platform` | Platform announcements, changelogs, navigation, lab list, search |
| `pwnbox` | PwnBox start/status/usage/terminate |
| `vm` | Spawn / wait / extend / reset / terminate / vote-reset / accept-vote / vpn-servers |
| `vpn` | List / switch / download / start / stop OpenVPN configs |
| `connection` | Current connections, server lists, switch, download UDP/TCP, prolab status |
| `review` | Mark a review helpful / unhelpful |
| `suspicious` | Profile-audit heuristics (analyze, score, speed, bursts, challenges) |
| `academyxlabs` | Academy ↔ Labs relations (modules, machines, exams, fortresses, prolabs, sherlocks) |

Discover everything with `uv run htbcli <group> --help`.

### Common conventions

Many list/profile commands accept these shared options:

- `--debug` — print the raw API response as a Rich panel
- `--json` — print the raw API response as JSON (great for piping into `jq`)
- `--responses` — print every field name returned by the endpoint
- `-o/--option <field>` — select specific fields (repeatable)

Most commands that take an entity (machine, challenge, sherlock, etc.) accept
either an ID or a slug/name.

## Examples

### Machines

```bash
# Currently active machine + VM status
uv run htbcli machines active

# List machines with filters
uv run htbcli machines list-machines --status active --difficulty easy --os linux
uv run htbcli machines list-machines --status retired --show-completed incomplete --sort-by rating --sort-type desc

# Paginated retired machines
uv run htbcli machines retired-list --page 2 --per-page 50 --free

# Search by name (substring match)
uv run htbcli machines search lame

# Profile by slug
uv run htbcli machines profile lame

# Tasks / guided mode for a retired machine
uv run htbcli machines tasks lame
uv run htbcli machines guided lame
uv run htbcli machines guided lame --show-hints

# Walkthroughs and writeups
uv run htbcli machines walkthroughs lame
uv run htbcli machines writeup lame

# Submit a flag (active machine, by ID, by name, or via stdin)
echo "FLAG{..}" | uv run htbcli machines submit
uv run htbcli machines submit "FLAG{..}"
uv run htbcli machines submit 12345 "FLAG{..}"
uv run htbcli machines submit lame "FLAG{..}"

# Submit an answer for a guided-mode task
uv run htbcli machines submit-task lame "answer" --task 42
```

Available filter values for `list-machines` / `retired-list`:

- `--status`: `active`, `retired`, `all`
- `--difficulty`: `very-easy`, `easy`, `medium`, `hard`, `insane` (repeatable)
- `--os`: `linux`, `windows`, `freebsd`, `openbsd`, `other` (repeatable)
- `--show-completed`: `complete`, `incomplete`
- `--sort-by`: `release-date`, `name`, `user-owns`, `system-owns`, `rating`, `user-difficulty`
- `--sort-type`: `asc`, `desc`
- `--free` (retired only), `--keyword`, `--tags <id>` (repeatable)

### Challenges

```bash
# List with filters
uv run htbcli challenges list-challenges --state active --difficulty medium --status incompleted --category web

# Info / categories / search
uv run htbcli challenges info my-challenge
uv run htbcli challenges categories
uv run htbcli challenges search reverse

# Download challenge files
uv run htbcli challenges download my-challenge -o files.zip

# Start / stop challenge instance
uv run htbcli challenges start my-challenge
uv run htbcli challenges stop my-challenge
uv run htbcli challenges active

# Todo list
uv run htbcli challenges todo-add my-challenge
uv run htbcli challenges todo-remove my-challenge
uv run htbcli challenges todo-cleanup

# Submit a flag (also accepts stdin)
uv run htbcli challenges submit my-challenge "HTB{...}"
echo "HTB{...}" | uv run htbcli challenges submit my-challenge
```

Filter values for `list-challenges`:

- `--state`: `active`, `retired`, `unreleased` (repeatable)
- `--status`: `incompleted`, `complete`
- `--difficulty`: `very-easy`, `easy`, `medium`, `hard`, `insane` (repeatable)
- `--category <id-or-name>` (repeatable; use `htbcli challenges categories` for IDs)
- `--sort-by`: `release-date`, `name`, `user-owns`, `system-owns`, `rating`, `user-difficulty`
- `--sort-type`: `asc`, `desc`
- `--todo`, `--clean-solved`

### Sherlocks

```bash
# List with filters
uv run htbcli sherlocks list-sherlocks --difficulty easy --state active --sort-by rating --sort-type desc

# Info / categories
uv run htbcli sherlocks info brutus
uv run htbcli sherlocks categories

# Download
uv run htbcli sherlocks download brutus
uv run htbcli sherlocks download brutus --link-only
uv run htbcli sherlocks download 123 -o brutus.zip

# Play / progress / tasks
uv run htbcli sherlocks play brutus
uv run htbcli sherlocks progress brutus
uv run htbcli sherlocks tasks brutus

# Submit flag for a specific task
uv run htbcli sherlocks submit-flag brutus 456 "FLAG{..}"

# Writeups
uv run htbcli sherlocks writeup brutus
uv run htbcli sherlocks writeup-official brutus
```

Filter values for `list-sherlocks`:

- `--difficulty`: `very-easy`, `easy`, `medium`, `hard`, `insane` (repeatable)
- `--state`: `active`, `retired`, `unreleased` (repeatable)
- `--category <id>` (repeatable)
- `--status`: `completed`, `incompleted`
- `--sort-by`: `solves`, `category`, `rating`, `name`
- `--sort-type`: `asc`, `desc`
- `--keyword`, `--todo`

### Fortresses & ProLabs

```bash
uv run htbcli fortresses list-fortresses
uv run htbcli fortresses info 1
uv run htbcli fortresses flags 1
uv run htbcli fortresses submit-flag 1 "FLAG{..}"
uv run htbcli fortresses reset 1

uv run htbcli prolabs list-prolabs
uv run htbcli prolabs info dante
uv run htbcli prolabs machines dante
uv run htbcli prolabs flags dante
uv run htbcli prolabs submit-flag dante "FLAG{..}"
uv run htbcli prolabs progress dante
uv run htbcli prolabs reviews dante
```

### Season

```bash
uv run htbcli season list-seasons
uv run htbcli season machines              # current season machines
uv run htbcli season machine-active        # active machines this season
uv run htbcli season completed <season-id>
uv run htbcli season rewards <season-id>
uv run htbcli season user-rank <season-id>
uv run htbcli season leaderboard <leaderboard-name>
uv run htbcli season leaderboard-top <leaderboard-name> <season-id>
uv run htbcli season end <season-id> <user-id>
uv run htbcli season user-followers <season-id>
```

Note: there is no dedicated `season submit` command — submit seasonal-machine
flags through `htbcli machines submit` against the active season machine.

### User

```bash
uv run htbcli user info                 # your own user info
uv run htbcli user profile 12345
uv run htbcli user activity 12345
uv run htbcli user bloods 12345
uv run htbcli user badges 12345
uv run htbcli user dashboard            # your dashboard
uv run htbcli user dashboard-tabloid
uv run htbcli user summary              # your summary
uv run htbcli user progress-machines-os 12345
uv run htbcli user progress-challenges 12345
uv run htbcli user progress-fortress 12345
uv run htbcli user progress-prolab 12345
uv run htbcli user progress-sherlocks 12345
uv run htbcli user followers            # your followers
uv run htbcli user follow 12345
uv run htbcli user unfollow 12345
uv run htbcli user respect 12345
uv run htbcli user disrespect 12345
uv run htbcli user banned               # check if your account is banned
uv run htbcli user settings
uv run htbcli user apptoken-list
uv run htbcli user achievement <target-type> <user-id> <target-id>
```

### VM Operations

```bash
# Spawn a VM (waits up to 5 minutes by default for it to be ready)
uv run htbcli vm spawn lame
uv run htbcli vm spawn lame --no-wait
uv run htbcli vm spawn lame --vpn-server 267 --max-wait 600

# Wait for a previously-spawned VM to come up
uv run htbcli vm wait lame --max-wait 300

# Extend / reset / terminate
uv run htbcli vm extend lame
uv run htbcli vm reset lame
uv run htbcli vm reset lame --no-wait
uv run htbcli vm terminate lame

# Reset voting
uv run htbcli vm vote-reset lame
uv run htbcli vm accept-vote lame

# List the VPN servers usable for spawning
uv run htbcli vm vpn-servers
```

`vm spawn` polls the API every 5 seconds until `isSpawning=False` and an IP is
assigned. Use `--no-wait` to spawn-and-exit immediately.

### VPN

The `vpn` group is **not** subcommand-based — it's a single command driven by
flags:

```bash
# List every VPN server (or filter by product)
uv run htbcli vpn --list
uv run htbcli vpn --list -p labs
uv run htbcli vpn --list -p starting_point
uv run htbcli vpn --list -p fortresses
uv run htbcli vpn --list -p competitive

# Switch the assigned server (use the ID column from --list)
uv run htbcli vpn --switch 267

# Download the OpenVPN config for the currently-selected server
uv run htbcli vpn -d
uv run htbcli vpn -d -p starting_point

# List previously downloaded VPN files (stored under ~/.htbcli/vpn)
uv run htbcli vpn --files

# Start / stop a VPN tunnel (requires sudo + openvpn installed)
uv run htbcli vpn --start --name "EU VIP 7" --mode labs
uv run htbcli vpn --stop
```

Live connection status is exposed by the `connection` group:

```bash
uv run htbcli connection status                 # currently active tunnels
uv run htbcli connection servers -p labs        # servers available for a product
uv run htbcli connection switch 267
uv run htbcli connection download-udp 267
uv run htbcli connection download-tcp 267
uv run htbcli connection product-status labs
uv run htbcli connection prolab-servers dante
uv run htbcli connection prolab-status dante
uv run htbcli connection connections            # last set connections
```

VPN start/stop requires the `openvpn` binary on your PATH and elevated
privileges (the CLI invokes `sudo openvpn` for you).

### Suspicious Activity Analysis

Heuristic auditing of an HTB profile (fast user→root times, burst sessions,
fast consecutive challenges, dormancy bursts, etc.):

```bash
uv run htbcli suspicious analyze <username-or-id>
uv run htbcli suspicious analyze <username-or-id> --release-dates  # slow, more accurate
uv run htbcli suspicious score <username-or-id>      # single 0-100 score
uv run htbcli suspicious speed <username-or-id>      # only fast user→root times
uv run htbcli suspicious bursts <username-or-id>     # burst sessions
uv run htbcli suspicious challenges <username-or-id> # fast consecutive challenges
```

All of the above accept `--debug` and `--json`.

### Academy ↔ Labs relations

Mirrors the dropdown on
[academy.hackthebox.com/academy-lab-relations](https://academy.hackthebox.com/academy-lab-relations):
pick any item from one of six categories (modules, machines, exams, fortresses,
prolabs, sherlocks) and see the related items in every other category. The
endpoints are public and unauthenticated, so this works without an HTB token.

```bash
# Quick lookup by category flag — accepts ID, slug, or (unique) name substring
uv run htbcli academyxlabs -m 'introduction to nosql injection'  # module -> 5 machines
uv run htbcli academyxlabs -M Mango                              # machine -> modules
uv run htbcli academyxlabs -e htb-certified-penetration-testing-specialist
uv run htbcli academyxlabs -f Jet                                # fortress
uv run htbcli academyxlabs -p RastaLabs                          # prolab
uv run htbcli academyxlabs -s Meerkat                            # sherlock

# Browse a whole category
uv run htbcli academyxlabs list modules
uv run htbcli academyxlabs list machines

# Explicit form (same effect as the flags above)
uv run htbcli academyxlabs relations modules introduction-to-nosql-injection
uv run htbcli academyxlabs relations machines 523

uv run htbcli academyxlabs categories                            # show flag table
```

## Shell Completion

Both bash and zsh are supported.

### Quick install

```bash
# From inside the repo (uses the bundled installer)
./install_completion.sh
```

The installer detects your shell, generates the completion script with
`htbcli completion --shell <bash|zsh> --raw`, backs up your `~/.bashrc` /
`~/.zshrc`, and appends the completion block.

### Manual install

```bash
# Print the script
uv run htbcli completion --shell bash         # human-readable preview
uv run htbcli completion --shell bash --raw   # raw script (source this)

# Source it for the current shell
source <(uv run htbcli completion --shell bash --raw)
source <(uv run htbcli completion --shell zsh --raw)

# Or append to your rc file
uv run htbcli completion --shell zsh --raw >> ~/.zshrc
```

Once installed, `htbcli <TAB>` will suggest commands, options and choice values.

## Configuration directory

State that the CLI writes is kept under `~/.htbcli/`:

- `~/.htbcli/.env` — optional `.env` file that is always loaded, regardless
  of your current working directory. Ideal for globally-installed binaries.
- `~/.htbcli/vpn/` — downloaded OpenVPN config files (`.ovpn`)

## Error Handling

- **Missing API Token** — `HTB_TOKEN environment variable not set`. Export
  `HTB_TOKEN` in your shell, or drop a `.env` file at `~/.htbcli/.env` (or
  in the current directory).
- **Rate limiting** — the API client enforces a minimum 1-second gap between
  requests automatically. Bulk operations (`--clean-solved`, large list pages)
  may still be throttled by the upstream API.
- **Invalid endpoint / network** — error messages include the HTTP status and
  upstream JSON body when available; rerun with `--debug` for the raw response.

## Project Structure

```
htbcli/
├── htbcli/
│   ├── __init__.py
│   ├── cli.py              # Click CLI root + top-level commands
│   ├── config.py           # HTB_TOKEN + API base URLs (loads ./.env and ~/.htbcli/.env)
│   ├── api_client.py       # Requests wrapper with rate limiting
│   ├── base_command.py     # Shared --debug / --json decorators
│   ├── swagger_parser.py   # Reads the bundled openapi.v4.yaml / swagger.json
│   ├── completion.py       # Runtime completion suggestions
│   ├── completion_script.py # bash/zsh completion script generators
│   └── modules/            # One file per command group
│       ├── machines.py
│       ├── challenges.py
│       ├── sherlocks.py
│       ├── fortresses.py
│       ├── prolabs.py
│       ├── season.py
│       ├── user.py
│       ├── team.py
│       ├── universities.py
│       ├── tracks.py
│       ├── starting_point.py
│       ├── ranking.py
│       ├── career.py
│       ├── badges.py
│       ├── home.py
│       ├── platform.py
│       ├── pwnbox.py
│       ├── vm.py
│       ├── vpn.py
│       ├── connection.py
│       ├── review.py
│       └── suspicious.py
├── htbcli.py               # Convenience launcher (`python htbcli.py ...`)
├── install_completion.sh
├── openapi.v4.yaml         # HTB API v4 spec used by `endpoints` / `module-info`
├── swagger.json
├── pyproject.toml
└── requirements.txt
```

## Development

### Adding a new module

1. Create a new file in `htbcli/modules/` — define an `XModule` class wrapping
   the API endpoints and a Click `@click.group()` exporting the commands.
2. Re-export both from `htbcli/modules/__init__.py`.
3. Import it in `htbcli/cli.py` and call `cli.add_command(your_group)`.

### Running tests

```bash
uv add --dev pytest pytest-cov
uv run pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License — see the `LICENSE` file for
details.

## Disclaimer

This project is not affiliated with or endorsed by HackTheBox. It's a
community-maintained tool for interacting with the HTB API.

## Changelog

### v1.4.1
- Added `LICENSE` file (MIT). The license was already declared in
  `pyproject.toml`, but the actual license text was missing from the repo.

### v1.4.0
- **New `academyxlabs` group.** Wraps the public
  `academy.hackthebox.com/api/v2/external/public/labs/...` endpoints behind
  the Academy x Labs relations page. Lookup any module / machine / exam /
  fortress / prolab / sherlock by ID, slug, or name and get every related
  item in every other category. No HTB token required.

### v1.3.0
- **Fixed `.env` auth for globally-installed users.** `Config` now also loads
  `~/.htbcli/.env` on import, so the `.env` workflow works from any directory
  (not just from the repo). An explicit `HTBCLI_ENV_FILE=/path/to/.env`
  override is also supported.
- **Single source of truth for version.** `__version__` is now read from the
  installed package metadata, so `htbcli --version`, `pyproject.toml` and the
  outgoing `User-Agent` header can no longer drift apart. The `User-Agent` is
  now `HTB-CLI/<version>` instead of the hardcoded `HTB-CLI/1.0.0`.
- **`htbcli setup` is no longer a no-op.** It creates `~/.htbcli/` and points
  you at the exact `.env` path the CLI will load.
- Removed the unused `CONFIG_FILE` JSON stub from `Config`.

### v1.2.0
- Added `suspicious` module for profile auditing
- VPN module rewritten as a flag-driven command (`--list`, `--start`, `--stop`,
  `--switch`, `-d`, `--files`)
- New `connection` module exposing live connection state, server lists and
  config downloads
- VM commands now wait for VMs to be ready by default; new `vm wait`,
  `vm vpn-servers`, and `--vpn-server` option for `vm spawn`
- Many new machine subcommands (`guided`, `submit-task`, `search`,
  `retired-list`, `walkthroughs`, `tasks`, `tags`, `creators`, `reviews`,
  `recommended`, `unreleased`, `todo-list`, `owns-top`, `owns-timeline`,
  `adventure`, etc.)
- Challenge module gained `download`, `start`, `stop`, `active`, `categories`,
  `todo-*`, `search`, `info`, `recommended`, `suggested`, writeups
- Sherlock filtering split `--state` from `--status`
- Filter values normalized to dash-case (`release-date`, `user-owns`, etc.)

### v1.0.0
- Initial release: Machines, Challenges, Users, Seasons, Sherlocks
- Rich-formatted CLI output
- Configuration via `HTB_TOKEN`
