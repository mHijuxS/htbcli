#!/bin/bash

# HTB CLI Auto-completion Demo Script

echo "🎯 HTB CLI Auto-completion Demo"
echo "================================"
echo ""

# Check if htbcli is available
if ! command -v htbcli &> /dev/null; then
    echo "❌ htbcli is not installed or not in PATH"
    echo "   Please install htbcli first"
    exit 1
fi

echo "✅ HTB CLI is available"
echo ""

# Show available commands
echo "📋 Available Commands:"
echo "======================"
htbcli --help | grep -E "^  [a-z]" | head -10
echo "... and more!"
echo ""

# Show completion setup
echo "🔧 Auto-completion Setup:"
echo "========================"
echo "1. Generate completion script:"
echo "   htbcli completion --shell bash"
echo "   htbcli completion --shell zsh"
echo ""
echo "2. Quick setup:"
echo "   ./install_completion.sh"
echo ""
echo "3. Manual setup:"
echo "   source <(htbcli completion --shell bash --raw)"
echo ""

# Show completion examples
echo "💡 Completion Examples:"
echo "======================"
echo "Once installed, you can use TAB completion:"
echo ""
echo "• htbcli [TAB]                    # Complete main commands"
echo "• htbcli machines [TAB]           # Complete machine subcommands"
echo "• htbcli challenges [TAB]         # Complete challenge subcommands"
echo "• htbcli machines list --[TAB]    # Complete options"
echo "• htbcli machines list-machines --difficulty [TAB]  # Complete choices (very-easy, easy, medium, hard, insane)"
echo "• htbcli machines list-machines --os [TAB] # Complete OS choices (linux, windows, freebsd, openbsd, other)"
echo "• htbcli machines list-machines --status [TAB] # Complete status choices (active, retired)"
echo "• htbcli machines retired-list --difficulty [TAB] # Complete choices (very-easy, easy, medium, hard, insane)"
echo "• htbcli challenges list-challenges --state [TAB] # Complete state choices (active, retired, unreleased)"
echo "• htbcli challenges list-challenges --status [TAB] # Complete status choices (incompleted, complete)"
echo ""

# Show what completion provides
echo "🎁 What Completion Provides:"
echo "==========================="
echo "• All main commands (machines, challenges, user, etc.)"
echo "• All subcommands (list-machines, retired-list, list-challenges, etc.)"
echo "• All options (--help, --debug, --json, etc.)"
echo "• Choice options (--difficulty, --os, --status, --state, --sort-by, etc.)"
echo "• Context-aware suggestions for machines and challenges"
echo "• Descriptive help (zsh)"
echo ""

echo "🚀 Ready to enhance your HTB CLI experience!"
echo "   Run: ./install_completion.sh to get started"
