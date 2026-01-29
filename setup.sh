#!/bin/bash
# InstaReelTranscriber - Unix Setup Script
# One-click setup for macOS and Linux

set -e

echo "============================================================"
echo "     InstaReelTranscriber - One-Click Setup"
echo "============================================================"

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8+ and try again."
    echo ""
    echo "macOS:  brew install python3"
    echo "Ubuntu: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the Python installer
echo "Running installer..."
$PYTHON_CMD "$SCRIPT_DIR/install.py" "$@"

exit $?
