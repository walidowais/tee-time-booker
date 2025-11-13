#!/bin/bash

# Replit startup script for tee time booking automation

echo "Setting up Tee Time Booking Automation for Replit..."

# Install system dependencies for Playwright
echo "Installing system dependencies..."
apt-get update
apt-get install -y wget gnupg
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium
playwright install-deps chromium

echo "Setup complete! Starting web server..."
python web_server.py
