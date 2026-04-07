#!/bin/bash

# Context Optimizer Installation Script
# Works on macOS and Linux

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Context Optimizer Installer${NC}"
echo "============================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
        echo "Please install Python 3.8+ from https://python.org"
        exit 1
    fi
    PYTHON=python
else
    PYTHON=python3
fi

# Check Python version
PYTHON_VERSION=$($PYTHON --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo -e "${RED}Error: Python 3.8+ is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Create installation directory
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Copy context_mapper.py
cp "$PROJECT_ROOT/tools/context_mapper.py" "$INSTALL_DIR/context-mapper"
chmod +x "$INSTALL_DIR/context-mapper"

echo -e "${GREEN}✓ Installed context-mapper to $INSTALL_DIR${NC}"

# Check if in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}Note: $INSTALL_DIR is not in your PATH${NC}"
    echo "Add this to your shell profile (.bashrc, .zshrc, etc.):"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then run: source ~/.bashrc (or your shell profile)"
fi

# Success message
echo ""
echo "============================"
echo -e "${GREEN}Installation Complete!${NC}"
echo "============================"
echo ""
echo "Usage:"
echo "  context-mapper /path/to/project"
echo ""
echo "Or run without installing:"
echo "  python3 $PROJECT_ROOT/tools/context_mapper.py /path/to/project"
echo ""
echo "Next steps:"
echo "  1. Generate a manifest: context-mapper ~/your-project"
echo "  2. Upload CONTEXT_MANIFEST.md to Claude Project"
echo "  3. Paste the one-click prompt from prompt/"
echo ""
echo -e "${BLUE}Happy optimizing!${NC}"
