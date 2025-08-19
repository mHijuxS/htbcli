"""
Auto-completion module for HTB CLI
"""

import os
import click
from typing import List, Dict, Any, Optional

def get_available_commands() -> List[str]:
    """Get list of all available top-level commands"""
    return [
        'machines', 'challenges', 'user', 'season', 'sherlocks',
        'badges', 'career', 'connection', 'fortresses', 'home',
        'platform', 'prolabs', 'pwnbox', 'ranking', 'review',
        'starting_point', 'team', 'tracks', 'universities', 'vm', 'vpn',
        'info', 'endpoints', 'module_info', 'setup'
    ]

def get_machine_subcommands() -> List[str]:
    """Get list of machine subcommands"""
    return [
        'list', 'active', 'info', 'submit', 'recommended', 'search',
        'activity', 'changelog', 'creators', 'graph-activity', 'graph-matrix',
        'graph-owns-difficulty', 'owns-top', 'reviews', 'reviews-user',
        'todo', 'todo-add', 'todo-remove', 'vpn-config', 'vpn-status',
        'vpn-connect', 'vpn-disconnect', 'spawn', 'terminate', 'status'
    ]

def get_challenge_subcommands() -> List[str]:
    """Get list of challenge subcommands"""
    return [
        'list-challenges', 'info', 'submit', 'categories', 'recommended',
        'suggested', 'activity', 'changelog', 'download', 'start', 'stop',
        'writeup', 'writeup-official', 'mark-helpful', 'search', 'reviews-user'
    ]

def get_user_subcommands() -> List[str]:
    """Get list of user subcommands"""
    return [
        'info', 'profile', 'activity', 'machines', 'challenges', 'sherlocks',
        'fortresses', 'prolabs', 'badges', 'career', 'ranking', 'reviews',
        'tracks', 'universities', 'connections', 'subscription', 'settings',
        'notifications', 'search', 'stats', 'owns', 'owns-top', 'owns-graph',
        'owns-difficulty', 'owns-os', 'owns-tags', 'owns-categories',
        'owns-seasons', 'owns-tracks', 'owns-universities', 'owns-fortresses',
        'owns-prolabs', 'owns-sherlocks', 'owns-badges', 'owns-career',
        'owns-ranking', 'owns-reviews', 'owns-connections', 'owns-subscription',
        'owns-settings', 'owns-notifications', 'owns-search', 'owns-stats'
    ]

def get_season_subcommands() -> List[str]:
    """Get list of season subcommands"""
    return [
        'list', 'info', 'machines', 'completed', 'leaderboard', 'stats',
        'rewards', 'badges', 'tracks', 'universities', 'fortresses',
        'prolabs', 'sherlocks', 'career', 'ranking', 'reviews'
    ]

def get_sherlocks_subcommands() -> List[str]:
    """Get list of sherlocks subcommands"""
    return [
        'list', 'categories', 'info', 'download-link', 'play', 'progress',
        'tasks', 'submit-flag', 'reviews', 'reviews-user', 'search'
    ]

def get_fortresses_subcommands() -> List[str]:
    """Get list of fortresses subcommands"""
    return [
        'list', 'info', 'submit-flag', 'reviews', 'reviews-user', 'search'
    ]

def get_prolabs_subcommands() -> List[str]:
    """Get list of prolabs subcommands"""
    return [
        'list', 'info', 'reviews', 'reviews-user', 'search'
    ]

def get_vm_subcommands() -> List[str]:
    """Get list of VM subcommands"""
    return [
        'spawn', 'terminate', 'status', 'list', 'info'
    ]

def get_vpn_subcommands() -> List[str]:
    """Get list of VPN subcommands"""
    return [
        'config', 'status', 'connect', 'disconnect'
    ]

def get_difficulty_choices() -> List[str]:
    """Get list of difficulty choices"""
    return ['very-easy', 'easy', 'medium', 'hard', 'insane']

def get_os_choices() -> List[str]:
    """Get list of OS choices"""
    return ['linux', 'windows', 'freebsd', 'openbsd', 'other']

def get_status_choices() -> List[str]:
    """Get list of status choices"""
    return ['active', 'retired', 'unreleased']

def get_sort_by_choices() -> List[str]:
    """Get list of sort by choices"""
    return ['release-date', 'name', 'user-owns', 'system-owns', 'rating', 'user-difficulty']

def get_sort_type_choices() -> List[str]:
    """Get list of sort type choices"""
    return ['asc', 'desc']

def get_show_completed_choices() -> List[str]:
    """Get list of show completed choices"""
    return ['complete', 'incomplete']

def get_challenge_status_choices() -> List[str]:
    """Get list of challenge status choices"""
    return ['incompleted', 'complete']

def get_challenge_state_choices() -> List[str]:
    """Get list of challenge state choices"""
    return ['active', 'retired', 'unreleased']

def get_challenge_sort_by_choices() -> List[str]:
    """Get list of challenge sort by choices"""
    return ['release-date', 'name', 'user-owns', 'system-owns', 'rating', 'user-difficulty']

def get_challenge_sort_type_choices() -> List[str]:
    """Get list of challenge sort type choices"""
    return ['asc', 'desc']

def get_challenge_difficulty_choices() -> List[str]:
    """Get list of challenge difficulty choices"""
    return ['very-easy', 'easy', 'medium', 'hard', 'insane']

def get_common_options() -> List[str]:
    """Get list of common options"""
    return [
        '--help', '--debug', '--json', '--responses', '--option', '-o',
        '--page', '--per-page', '--sort-by', '--sort-type', '--difficulty',
        '--os', '--tags', '--keyword', '--show-completed', '--free',
        '--status', '--state', '--category', '--todo', '--max-pages',
        '--output', '-o', '--count-only'
    ]

def get_machine_names() -> List[str]:
    """Get list of machine names from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_challenge_names() -> List[str]:
    """Get list of challenge names from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_user_names() -> List[str]:
    """Get list of user names from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_season_ids() -> List[str]:
    """Get list of season IDs from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_sherlock_ids() -> List[str]:
    """Get list of sherlock IDs from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_fortress_ids() -> List[str]:
    """Get list of fortress IDs from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_prolab_ids() -> List[str]:
    """Get list of prolab IDs from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_category_ids() -> List[str]:
    """Get list of category IDs from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_tag_ids() -> List[str]:
    """Get list of tag IDs from API"""
    # For now, return empty list to avoid API calls during completion
    # This can be enhanced later with caching or lazy loading
    return []

def get_completion_suggestions(ctx: click.Context, args: List[str], incomplete: str) -> List[str]:
    """Get completion suggestions based on current context"""
    suggestions = []
    
    # If no arguments yet, suggest top-level commands
    if len(args) == 0:
        suggestions = [cmd for cmd in get_available_commands() if cmd.startswith(incomplete)]
    
    # If one argument, suggest subcommands based on the command
    elif len(args) == 1:
        command = args[0]
        
        if command == 'machines':
            suggestions = [subcmd for subcmd in get_machine_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'challenges':
            suggestions = [subcmd for subcmd in get_challenge_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'user':
            suggestions = [subcmd for subcmd in get_user_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'season':
            suggestions = [subcmd for subcmd in get_season_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'sherlocks':
            suggestions = [subcmd for subcmd in get_sherlocks_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'fortresses':
            suggestions = [subcmd for subcmd in get_fortresses_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'prolabs':
            suggestions = [subcmd for subcmd in get_prolabs_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'vm':
            suggestions = [subcmd for subcmd in get_vm_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'vpn':
            suggestions = [subcmd for subcmd in get_vpn_subcommands() if subcmd.startswith(incomplete)]
        elif command == 'module_info':
            # For module_info, suggest module names
            suggestions = [cmd for cmd in get_available_commands() if cmd.startswith(incomplete) and cmd not in ['info', 'endpoints', 'setup', 'module_info']]
    
    # If two or more arguments, suggest based on the specific command and subcommand
    elif len(args) >= 2:
        command = args[0]
        subcommand = args[1]
        
        # Machine-specific suggestions
        if command == 'machines':
            if subcommand in ['info', 'submit', 'activity', 'changelog', 'creators', 'graph-activity', 'graph-matrix', 'graph-owns-difficulty', 'owns-top', 'reviews', 'reviews-user', 'todo', 'todo-add', 'todo-remove', 'spawn', 'terminate', 'status']:
                suggestions = get_machine_names()
            elif subcommand == 'list':
                suggestions = get_common_options()
        
        # Challenge-specific suggestions
        elif command == 'challenges':
            if subcommand in ['info', 'submit', 'activity', 'changelog', 'download', 'start', 'stop', 'writeup', 'writeup-official', 'mark-helpful', 'reviews-user']:
                suggestions = get_challenge_names()
            elif subcommand == 'list-challenges':
                suggestions = get_common_options()
        
        # User-specific suggestions
        elif command == 'user':
            if subcommand in ['info', 'profile', 'activity', 'machines', 'challenges', 'sherlocks', 'fortresses', 'prolabs', 'badges', 'career', 'ranking', 'reviews', 'tracks', 'universities', 'connections', 'subscription', 'settings', 'notifications', 'search', 'stats', 'owns', 'owns-top', 'owns-graph', 'owns-difficulty', 'owns-os', 'owns-tags', 'owns-categories', 'owns-seasons', 'owns-tracks', 'owns-universities', 'owns-fortresses', 'owns-prolabs', 'owns-sherlocks', 'owns-badges', 'owns-career', 'owns-ranking', 'owns-reviews', 'owns-connections', 'owns-subscription', 'owns-settings', 'owns-notifications', 'owns-search', 'owns-stats']:
                suggestions = get_user_names()
        
        # Season-specific suggestions
        elif command == 'season':
            if subcommand in ['info', 'machines', 'completed', 'leaderboard', 'stats', 'rewards', 'badges', 'tracks', 'universities', 'fortresses', 'prolabs', 'sherlocks', 'career', 'ranking', 'reviews']:
                suggestions = get_season_ids()
        
        # Sherlocks-specific suggestions
        elif command == 'sherlocks':
            if subcommand in ['info', 'download-link', 'play', 'progress', 'tasks', 'submit-flag', 'reviews', 'reviews-user']:
                suggestions = get_sherlock_ids()
        
        # Fortresses-specific suggestions
        elif command == 'fortresses':
            if subcommand in ['info', 'submit-flag', 'reviews', 'reviews-user']:
                suggestions = get_fortress_ids()
        
        # Prolabs-specific suggestions
        elif command == 'prolabs':
            if subcommand in ['info', 'reviews', 'reviews-user']:
                suggestions = get_prolab_ids()
        
        # Common option suggestions for any command
        if incomplete.startswith('-'):
            suggestions.extend([opt for opt in get_common_options() if opt.startswith(incomplete)])
        
        # Choice-based suggestions
        if '--difficulty' in args:
            suggestions.extend(get_difficulty_choices())
        elif '--os' in args:
            suggestions.extend(get_os_choices())
        elif '--status' in args:
            suggestions.extend(get_status_choices())
        elif '--sort-by' in args:
            suggestions.extend(get_sort_by_choices())
        elif '--sort-type' in args:
            suggestions.extend(get_sort_type_choices())
        elif '--show-completed' in args:
            suggestions.extend(get_show_completed_choices())
        elif '--category' in args:
            suggestions.extend(get_category_ids())
        elif '--tags' in args:
            suggestions.extend(get_tag_ids())
    
    return [s for s in suggestions if s.startswith(incomplete)]

def setup_completion():
    """Setup completion for the CLI"""
    # This function can be called to setup completion
    # In a real implementation, this would register the completion function
    pass
