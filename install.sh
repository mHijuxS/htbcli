#!/bin/bash

# HTB CLI Installation Script

echo "🚀 Installing HTB CLI..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
uv venv
uv pip install -r requirements.txt

# Install the package in development mode
echo "🔧 Installing HTB CLI package..."
uv pip install -e .

echo "✅ Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Get your API token from https://app.hackthebox.com"
echo "2. Set the environment variable: export HTB_TOKEN='your_token_here'"
echo "3. Or create a .env file with: HTB_TOKEN=your_token_here"
echo "4. Run '.venv/bin/htbcli info' to verify your configuration"
echo ""
echo "🎉 You can now use the CLI with: .venv/bin/htbcli"
