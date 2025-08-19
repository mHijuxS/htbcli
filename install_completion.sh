#!/bin/bash

# HTB CLI Auto-completion Installation Script

echo "🚀 Installing HTB CLI Auto-completion..."

# Check if htbcli is available
if ! command -v htbcli &> /dev/null; then
    echo "❌ htbcli is not installed or not in PATH"
    echo "   Please install htbcli first and ensure it's in your PATH"
    exit 1
fi

# Detect shell
SHELL_NAME=$(basename "$SHELL")
echo "📋 Detected shell: $SHELL_NAME"

# Check if shell is supported
if [[ "$SHELL_NAME" != "bash" && "$SHELL_NAME" != "zsh" ]]; then
    echo "❌ Shell '$SHELL_NAME' is not supported"
    echo "   Supported shells: bash, zsh"
    exit 1
fi

# Determine shell config file
if [[ "$SHELL_NAME" == "bash" ]]; then
    SHELL_RC="$HOME/.bashrc"
elif [[ "$SHELL_NAME" == "zsh" ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

echo "📝 Shell config file: $SHELL_RC"

# Check if completion is already installed
if grep -q "htbcli.*completion" "$SHELL_RC" 2>/dev/null; then
    echo "⚠️  HTB CLI completion appears to be already installed in $SHELL_RC"
    read -p "Do you want to reinstall it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled"
        exit 0
    fi
fi

# Generate completion script
echo "🔧 Generating completion script..."
COMPLETION_SCRIPT=$(htbcli completion --shell "$SHELL_NAME" --raw)

if [ $? -ne 0 ]; then
    echo "❌ Failed to generate completion script"
    exit 1
fi

# Create backup of shell config
BACKUP_FILE="${SHELL_RC}.backup.$(date +%Y%m%d_%H%M%S)"
echo "💾 Creating backup: $BACKUP_FILE"
cp "$SHELL_RC" "$BACKUP_FILE"

# Remove existing htbcli completion if present
echo "🧹 Removing existing htbcli completion..."
sed -i '/# HTB CLI.*completion/,/complete -F _htbcli_completion htbcli/d' "$SHELL_RC" 2>/dev/null
sed -i '/# HTB CLI.*completion/,/compdef _htbcli htbcli/d' "$SHELL_RC" 2>/dev/null

# Add completion script to shell config
echo "📝 Adding completion script to $SHELL_RC..."
echo "" >> "$SHELL_RC"
echo "# HTB CLI Auto-completion" >> "$SHELL_RC"
echo "$COMPLETION_SCRIPT" >> "$SHELL_RC"

echo "✅ HTB CLI auto-completion installed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Restart your terminal or run: source $SHELL_RC"
echo "2. Test completion by typing: htbcli [TAB]"
echo "3. Try: htbcli machines [TAB] to see subcommands"
echo ""
echo "🎉 Enjoy your enhanced HTB CLI experience!"
echo ""
echo "💡 Tips:"
echo "   - Use TAB to cycle through suggestions"
echo "   - Use [TAB][TAB] to see all available options"
echo "   - Completion works for commands, subcommands, and options"
echo ""
echo "🔄 To uninstall, remove the HTB CLI completion section from $SHELL_RC"
