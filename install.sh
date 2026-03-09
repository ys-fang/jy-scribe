#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

echo "=== jy-scribe installer ==="

# Check ffmpeg
if ! command -v ffmpeg &>/dev/null; then
    echo "Error: ffmpeg not found. Install with: brew install ffmpeg"
    exit 1
fi

# Find Python 3.12+
if command -v python3.12 &>/dev/null; then
    PYTHON_CMD="python3.12"
elif command -v /opt/homebrew/bin/python3.12 &>/dev/null; then
    PYTHON_CMD="/opt/homebrew/bin/python3.12"
else
    echo "Error: Python 3.12+ required. Install with: brew install python@3.12"
    exit 1
fi
echo "Using: $PYTHON_CMD ($($PYTHON_CMD --version))"

# Create venv
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python venv..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

# Activate and install
source "$VENV_DIR/bin/activate"
echo "Upgrading pip..."
pip install --upgrade pip
echo "Installing dependencies..."
pip install -e .
pip install pytest

echo ""
echo "=== Installation complete ==="
echo "Activate with: source $VENV_DIR/bin/activate"
echo "Run with: jy-scribe <audio-file>"
