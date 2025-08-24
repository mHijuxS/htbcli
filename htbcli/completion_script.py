"""
Shell completion script generator for HTB CLI
"""

import os
import sys
import subprocess
from typing import List, Dict, Any

def get_htbcli_commands() -> List[str]:
    """Get all available htbcli commands"""
    try:
        result = subprocess.run(['htbcli', '--help'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            commands = []
            for line in lines:
                if line.strip() and not line.startswith('Usage:') and not line.startswith('Options:'):
                    # Extract command names from help output
                    parts = line.strip().split()
                    if parts and not parts[0].startswith('-'):
                        commands.append(parts[0])
            return [cmd for cmd in commands if cmd and not cmd.startswith('-')]
    except:
        pass
    return []

def get_htbcli_subcommands(command: str) -> List[str]:
    """Get subcommands for a specific command"""
    try:
        result = subprocess.run(['htbcli', command, '--help'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            subcommands = []
            for line in lines:
                if line.strip() and not line.startswith('Usage:') and not line.startswith('Options:'):
                    parts = line.strip().split()
                    if parts and not parts[0].startswith('-'):
                        subcommands.append(parts[0])
            return [subcmd for subcmd in subcommands if subcmd and not subcmd.startswith('-')]
    except:
        pass
    return []

def generate_bash_completion() -> str:
    """Generate bash completion script"""
    return """# HTB CLI bash completion
_htbcli_completion() {
    local cur prev opts cmd subcmd
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Get command and subcommand
    cmd="${COMP_WORDS[1]}"
    subcmd="${COMP_WORDS[2]}"
    
    # Get all available commands
    if [ $COMP_CWORD -eq 1 ]; then
        opts="machines challenges user season sherlocks badges career connection fortresses home platform prolabs pwnbox ranking review starting_point team tracks universities vm vpn info endpoints module_info setup completion"
        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
        return 0
    fi
    
    # Handle subcommands
    if [ $COMP_CWORD -eq 2 ]; then
        case $cmd in
            machines)
                opts="active activity adventure changelog creators graph-activity graph-difficulty graph-matrix list-machines machine-tags owns-top profile recommended recommended-retired retired-list reviews reviews-user submit tags tasks todo-list unreleased walkthrough-feedback-choices walkthrough-languages walkthrough-random walkthroughs writeup"
                ;;
            challenges)
                opts="list-challenges info submit categories recommended suggested activity changelog download start stop writeup writeup-official mark-helpful search reviews-user"
                ;;
            user)
                opts="info profile activity machines challenges sherlocks fortresses prolabs badges career ranking reviews tracks universities connections subscription settings notifications search stats owns owns-top owns-graph owns-difficulty owns-os owns-tags owns-categories owns-seasons owns-tracks owns-universities owns-fortresses owns-prolabs owns-sherlocks owns-badges owns-career owns-ranking owns-reviews owns-connections owns-subscription owns-settings owns-notifications owns-search owns-stats"
                ;;
            season)
                opts="list info machines completed leaderboard stats rewards badges tracks universities fortresses prolabs sherlocks career ranking reviews"
                ;;
            sherlocks)
                opts="list categories info download-link play progress tasks submit-flag reviews reviews-user search"
                ;;
            fortresses)
                opts="list info submit-flag reviews reviews-user search"
                ;;
            prolabs)
                opts="changelogs connection flags info list-prolabs machines overview progress reviews submit-flag"
                ;;
            vm)
                opts="spawn terminate status list info"
                ;;
            vpn)
                opts="config status connect disconnect"
                ;;
            *)
                opts=""
                ;;
        esac
        COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
        return 0
    fi
    
    # Handle option values based on context
    case $prev in
        # Machine options
        --difficulty)
            if [ "$cmd" = "machines" ]; then
                opts="very-easy easy medium hard insane"
            elif [ "$cmd" = "challenges" ]; then
                opts="very-easy easy medium hard insane"
            else
                opts="very-easy easy medium hard insane"
            fi
            ;;
        --os)
            opts="linux windows freebsd openbsd other"
            ;;
        --status)
            if [ "$cmd" = "machines" ]; then
                opts="active retired"
            elif [ "$cmd" = "challenges" ]; then
                opts="incompleted complete"
            else
                opts="active retired unreleased"
            fi
            ;;
        --sort-by)
            opts="release-date name user-owns system-owns rating user-difficulty"
            ;;
        --sort-type)
            opts="asc desc"
            ;;
        --show-completed)
            opts="complete incomplete"
            ;;
        --state)
            opts="active retired unreleased"
            ;;
        # PwnBox options
        --location)
            opts="us-east us-west uk ca in de au"
            ;;
        # Common options
        --help|--debug|--json|--responses|--option|-o|--page|--per-page|--tags|--keyword|--free|--category|--todo|--max-pages|--output|--count-only)
            # These don't need value completion
            opts=""
            ;;
        *)
            # Default: suggest common options
            opts="--help --debug --json --responses --option -o --page --per-page --sort-by --sort-type --difficulty --os --tags --keyword --show-completed --free --status --state --category --todo --max-pages --output --count-only"
            ;;
    esac
    
    COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
    return 0
}

complete -F _htbcli_completion htbcli
"""

def generate_zsh_completion() -> str:
    """Generate zsh completion script"""
    return """# HTB CLI zsh completion
_htbcli() {
    local curcontext="$curcontext" state line
    typeset -A opt_args
    
    _arguments -C \\
        '1: :->cmds' \\
        '*:: :->args'
    
    case $state in
        cmds)
            _htbcli_commands
            ;;
        args)
            _htbcli_arguments
            ;;
    esac
}

_htbcli_commands() {
    local commands
    commands=(
        'machines:Machine-related commands'
        'challenges:Challenge-related commands'
        'user:User-related commands'
        'season:Season-related commands'
        'sherlocks:Sherlock-related commands'
        'badges:Badge-related commands'
        'career:Career-related commands'
        'connection:Connection-related commands'
        'fortresses:Fortress-related commands'
        'home:Home-related commands'
        'platform:Platform-related commands'
        'prolabs:ProLab-related commands'
        'pwnbox:PwnBox-related commands'
        'ranking:Ranking-related commands'
        'review:Review-related commands'
        'starting_point:Starting Point-related commands'
        'team:Team-related commands'
        'tracks:Track-related commands'
        'universities:University-related commands'
        'vm:VM-related commands'
        'vpn:VPN-related commands'
        'info:Show HTB CLI information'
        'endpoints:List all available API endpoints'
        'module_info:Show detailed information about a module'
        'setup:Setup HTB CLI configuration'
        'completion:Generate shell completion script'
    )
    _describe -t commands 'htbcli commands' commands
}

_htbcli_arguments() {
    local curcontext="$curcontext" state line
    typeset -A opt_args
    
    _arguments -C \\
        '1: :->subcmds' \\
        '*:: :->subargs'
    
    case $state in
        subcmds)
            _htbcli_subcommands
            ;;
        subargs)
            # Route to specific completion functions based on command and subcommand
            if [[ "$words[1]" == "machines" ]]; then
                _htbcli_machines_list
            elif [[ "$words[1]" == "challenges" ]]; then
                _htbcli_challenges_list
            else
                _htbcli_subarguments
            fi
            ;;
    esac
}

_htbcli_subcommands() {
    local subcommands
    case $words[1] in
        machines)
            subcommands=(
                'active:Get currently active machine and VM status'
                'activity:Get machine activity'
                'adventure:Get machine adventure'
                'changelog:Get machine changelog'
                'creators:Get machine creators'
                'graph-activity:Get machine graph activity'
                'graph-difficulty:Get machine graph difficulty'
                'graph-matrix:Get machine graph matrix'
                'list-machines:List machines with filtering options'
                'machine-tags:Get machine tags'
                'owns-top:Get top 25 owners for a machine'
                'profile:Get machine profile by slug'
                'recommended:Get recommended machines'
                'recommended-retired:Get recommended retired machines'
                'retired-list:Get paginated list of retired machines'
                'reviews:Get machine reviews'
                'reviews-user:Get user review for machine'
                'submit:Submit flag for machine'
                'tags:Get machine tags list'
                'tasks:Get machine tasks'
                'todo-list:Get machine todo list'
                'unreleased:Get unreleased machines'
                'walkthrough-feedback-choices:Get walkthrough feedback choices'
                'walkthrough-languages:Get walkthrough language options'
                'walkthrough-random:Get random walkthrough'
                'walkthroughs:Get machine walkthroughs'
                'writeup:Get machine writeup'
            )
            ;;
        challenges)
            subcommands=(
                'list-challenges:List challenges'
                'info:Get challenge info'
                'submit:Submit challenge flag'
                'categories:Get challenge categories'
                'recommended:Get recommended challenges'
                'suggested:Get suggested challenges'
                'activity:Get challenge activity'
                'changelog:Get challenge changelog'
                'download:Download challenge files'
                'start:Start challenge'
                'stop:Stop challenge'
                'writeup:Get challenge writeup'
                'writeup-official:Get official challenge writeup'
                'mark-helpful:Mark review as helpful'
                'search:Search for challenges'
                'reviews-user:Get user challenge reviews'
            )
            ;;
        user)
            subcommands=(
                'info:Get user info'
                'profile:Get user profile'
                'activity:Get user activity'
                'machines:Get user machines'
                'challenges:Get user challenges'
                'sherlocks:Get user sherlocks'
                'fortresses:Get user fortresses'
                'prolabs:Get user prolabs'
                'badges:Get user badges'
                'career:Get user career'
                'ranking:Get user ranking'
                'reviews:Get user reviews'
                'tracks:Get user tracks'
                'universities:Get user universities'
                'connections:Get user connections'
                'subscription:Get user subscription'
                'settings:Get user settings'
                'notifications:Get user notifications'
                'search:Search for users'
                'stats:Get user stats'
                'owns:Get user owns'
                'owns-top:Get user top owns'
                'owns-graph:Get user owns graph'
                'owns-difficulty:Get user owns difficulty'
                'owns-os:Get user owns OS'
                'owns-tags:Get user owns tags'
                'owns-categories:Get user owns categories'
                'owns-seasons:Get user owns seasons'
                'owns-tracks:Get user owns tracks'
                'owns-universities:Get user owns universities'
                'owns-fortresses:Get user owns fortresses'
                'owns-prolabs:Get user owns prolabs'
                'owns-sherlocks:Get user owns sherlocks'
                'owns-badges:Get user owns badges'
                'owns-career:Get user owns career'
                'owns-ranking:Get user owns ranking'
                'owns-reviews:Get user owns reviews'
                'owns-connections:Get user owns connections'
                'owns-subscription:Get user owns subscription'
                'owns-settings:Get user owns settings'
                'owns-notifications:Get user owns notifications'
                'owns-search:Get user owns search'
                'owns-stats:Get user owns stats'
            )
            ;;
        season)
            subcommands=(
                'list:List seasons'
                'info:Get season info'
                'machines:Get season machines'
                'completed:Get completed machines'
                'leaderboard:Get season leaderboard'
                'stats:Get season stats'
                'rewards:Get season rewards'
                'badges:Get season badges'
                'tracks:Get season tracks'
                'universities:Get season universities'
                'fortresses:Get season fortresses'
                'prolabs:Get season prolabs'
                'sherlocks:Get season sherlocks'
                'career:Get season career'
                'ranking:Get season ranking'
                'reviews:Get season reviews'
            )
            ;;
        sherlocks)
            subcommands=(
                'list:List sherlocks'
                'categories:Get sherlock categories'
                'info:Get sherlock info'
                'download-link:Get sherlock download link'
                'play:Play sherlock'
                'progress:Get sherlock progress'
                'tasks:Get sherlock tasks'
                'submit-flag:Submit sherlock flag'
                'reviews:Get sherlock reviews'
                'reviews-user:Get user sherlock reviews'
                'search:Search for sherlocks'
            )
            ;;
        fortresses)
            subcommands=(
                'list:List fortresses'
                'info:Get fortress info'
                'submit-flag:Submit fortress flag'
                'reviews:Get fortress reviews'
                'reviews-user:Get user fortress reviews'
                'search:Search for fortresses'
            )
            ;;
        prolabs)
            subcommands=(
                'changelogs:Get prolab changelogs'
                'connection:Get prolab connection information'
                'flags:Get prolab flags'
                'info:Get prolab info by identifier/name'
                'list-prolabs:List prolabs'
                'machines:Get prolab machines'
                'overview:Get prolab overview'
                'progress:Get prolab progress'
                'reviews:Get prolab reviews'
                'submit-flag:Submit a flag for a prolab'
            )
            ;;
        vm)
            subcommands=(
                'spawn:Spawn VM'
                'terminate:Terminate VM'
                'status:Get VM status'
                'list:List VMs'
                'info:Get VM info'
            )
            ;;
        vpn)
            subcommands=(
                'config:Get VPN config'
                'status:Get VPN status'
                'connect:Connect to VPN'
                'disconnect:Disconnect from VPN'
            )
            ;;
        *)
            subcommands=()
            ;;
    esac
    
    if [ ${#subcommands} -gt 0 ]; then
        _describe -t subcommands 'htbcli subcommands' subcommands
    fi
}

_htbcli_subarguments() {
    _arguments \
        '--help[Show help]' \
        '--debug[Show debug info]' \
        '--json[Output as JSON]' \
        '--page[Page number]:page number:' \
        '--per-page[Results per page]:per page:' \
        '--sort-by[Sort by field]:field:(release-date name user-owns system-owns rating user-difficulty)' \
        '--sort-type[Sort type]:order:(asc desc)' \
        '--difficulty[Difficulty filter]:difficulty:(very-easy easy medium hard insane)' \
        '--os[OS filter]:os:(linux windows freebsd openbsd other)' \
        '--tags[Tags filter]:tag:' \
        '--keyword[Keyword search]:keyword:' \
        '--show-completed[Show completed items]:completed:(complete incomplete)' \
        '--free[Show free items only]' \
        '--status[Status filter]:status:(incompleted complete)' \
        '--state[State filter]:state:(active retired unreleased)' \
        '--category[Category filter]:category:' \
        '--todo[Show todo items only]' \
        '--max-pages[Maximum pages to search]:pages:' \
        '--output[Output file]:file:_files' \
        '--count-only[Show count only]' \
        '--responses[Show all response fields]' \
        '--option[Show specific fields]:field:' \
        '-o[Show specific fields]:field:'
}

# Enhanced completion for specific commands with option values
_htbcli_machines_list() {
    _arguments -C \
        '--help[Show help]' \
        '--debug[Show debug info]' \
        '--json[Output as JSON]' \
        '--page[Page number]:page number:' \
        '--per-page[Results per page]:per page:' \
        '--status[Status filter]:status:(active retired)' \
        '--sort-by[Sort by field]:field:(release-date name user-owns system-owns rating user-difficulty)' \
        '--sort-type[Sort type]:order:(asc desc)' \
        '--difficulty[Difficulty filter]:difficulty:(very-easy easy medium hard insane)' \
        '--os[OS filter]:os:(linux windows freebsd openbsd other)' \
        '--tags[Tags filter]:tag:' \
        '--keyword[Keyword search]:keyword:' \
        '--show-completed[Show completed items]:completed:(complete incomplete)' \
        '--free[Show free items only]' \
        '--responses[Show all response fields]' \
        '--option[Show specific fields]:field:' \
        '-o[Show specific fields]:field:'
    
    case $state in
    esac
}

_htbcli_machines_retired_list() {
    _arguments -C \
        '--help[Show help]' \
        '--debug[Show debug info]' \
        '--json[Output as JSON]' \
        '--page[Page number]:page number:' \
        '--per-page[Results per page]:per page:' \
        '--sort-by[Sort by field]:field:(release-date name user-owns system-owns rating user-difficulty)' \
        '--sort-type[Sort type]:order:(asc desc)' \
        '--difficulty[Difficulty filter]:difficulty:(very-easy easy medium hard insane)' \
        '--os[OS filter]:os:(linux windows freebsd openbsd other)' \
        '--tags[Tags filter]:tag:' \
        '--keyword[Keyword search]:keyword:' \
        '--show-completed[Show completed items]:completed:(complete incomplete)' \
        '--free[Show free items only]'
    
    case $state in
    esac
}

_htbcli_challenges_list() {
    _arguments -C \
        '--help[Show help]' \
        '--debug[Show debug info]' \
        '--json[Output as JSON]' \
        '--page[Page number]:page number:' \
        '--per-page[Results per page]:per page:' \
        '--status[Status filter]:status:(incompleted complete)' \
        '--state[State filter]:state:(active retired unreleased)' \
        '--sort-by[Sort by field]:field:(release-date name user-owns system-owns rating user-difficulty)' \
        '--sort-type[Sort type]:order:(asc desc)' \
        '--difficulty[Difficulty filter]:difficulty:(very-easy easy medium hard insane)' \
        '--category[Category filter]:category:' \
        '--todo[Show todo items only]' \
        '--responses[Show all response fields]' \
        '--option[Show specific fields]:field:' \
        '-o[Show specific fields]:field:'
}

# Add option value completions
_htbcli_option_values() {
    local option=$1
    local values
    
    case $option in
        --difficulty|--challenge-difficulty)
            values=('very-easy:Very Easy' 'easy:Easy' 'medium:Medium' 'hard:Hard' 'insane:Insane')
            ;;
        --os)
            values=('linux:Linux' 'windows:Windows' 'freebsd:FreeBSD' 'openbsd:OpenBSD' 'other:Other')
            ;;
        --status)
            if [[ $words[1] == "challenges" ]]; then
                values=('incompleted:Incompleted' 'complete:Complete')
            elif [[ $words[1] == "machines" ]]; then
                values=('active:Active' 'retired:Retired')
            else
                values=('active:Active' 'retired:Retired' 'unreleased:Unreleased')
            fi
            ;;
        --state|--challenge-state)
            values=('active:Active' 'retired:Retired' 'unreleased:Unreleased')
            ;;
        --sort-by|--challenge-sort-by)
            values=('release-date:Release Date' 'name:Name' 'user-owns:User Owns' 'system-owns:System Owns' 'rating:Rating' 'user-difficulty:User Difficulty')
            ;;
        --sort-type|--challenge-sort-type)
            values=('asc:Ascending' 'desc:Descending')
            ;;
        --show-completed)
            values=('complete:Complete' 'incomplete:Incomplete')
            ;;
        --location)
            values=('us-east:US East' 'us-west:US West' 'uk:UK' 'ca:Canada' 'in:India' 'de:Germany' 'au:Australia')
            ;;
        *)
            values=()
            ;;
    esac
    
    if [[ ${#values} -gt 0 ]]; then
        _describe -t values "option values" values
    fi
}

# Ensure completion system is loaded
autoload -Uz compinit
compinit

# Register completion function
compdef _htbcli htbcli
"""

def main():
    """Main function to generate completion scripts"""
    if len(sys.argv) < 2:
        print("Usage: python completion_script.py [bash|zsh]")
        sys.exit(1)
    
    shell = sys.argv[1].lower()
    
    if shell == 'bash':
        print(generate_bash_completion())
    elif shell == 'zsh':
        print(generate_zsh_completion())
    else:
        print(f"Unsupported shell: {shell}")
        print("Supported shells: bash, zsh")
        sys.exit(1)

if __name__ == '__main__':
    main()
