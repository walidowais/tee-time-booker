#!/usr/bin/env python3
"""
Main entry point for Replit
This file ensures Replit starts the web server correctly
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return False
    return True

def start_server():
    """Start the web server"""
    print("Starting web server...")
    try:
        # Import and run the web server
        from web_server import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except ImportError as e:
        print(f"Import error: {e}")
        print("Trying to install Flask...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "gunicorn", "requests"])
        from web_server import app
        app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    print("🚀 Starting Tee Time Booking Automation Server...")

    # Install dependencies first
    if install_dependencies():
        start_server()
    else:
        print("❌ Failed to install dependencies")
        sys.exit(1)
