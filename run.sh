#!/bin/bash

# Simple run script for tee time booking automation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment and run the script
echo "Starting tee time booking automation..."
source venv/bin/activate
python tee_time_booker.py
