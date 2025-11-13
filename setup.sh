#!/bin/bash

# Tee Time Booking Automation Setup Script

echo "Setting up Tee Time Booking Automation..."

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

echo ""
echo "Setup complete!"
echo ""
echo "To run the tee time booker:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the script: python tee_time_booker.py"
echo ""
echo "Note: The script will open a browser window so you can see what's happening."
echo "You can modify the script to run in headless mode by changing 'headless=False' to 'headless=True'"
