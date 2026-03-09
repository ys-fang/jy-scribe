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

# Create venv
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python venv..."
    python3 -m venv "$VENV_DIR"
fi

# Activate and install
source "$VENV_DIR/bin/activate"
echo "Installing dependencies..."
pip install -e ".[dev]" 2>/dev/null || pip install -e .
pip install pytest

echo ""
echo "=== Installation complete ==="
echo "Activate with: source $VENV_DIR/bin/activate"
echo "Run with: jy-scribe <audio-file>"
