#!/usr/bin/env python3
"""
Web Server for Tee Time Booking Automation

This Flask app provides a web endpoint that can be triggered by cron-job.org
to automatically run the tee time booking script.
"""

import asyncio
import threading
import logging
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from tee_time_booker import TeeTimeBooker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variable to track if a booking is currently running
booking_in_progress = False
last_booking_result = {"status": "none", "timestamp": None, "message": "No bookings attempted yet"}

def run_booking_async():
    """Run the booking automation in a separate thread"""
    global booking_in_progress, last_booking_result

    try:
        booking_in_progress = True
        logger.info("Starting tee time booking automation...")

        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run the booking automation
        booker = TeeTimeBooker()
        # Set headless mode for cloud environment
        booker.headless = True

        result = loop.run_until_complete(booker.run())

        last_booking_result = {
            "status": "success" if result else "failed",
            "timestamp": datetime.now().isoformat(),
            "message": "Booking completed successfully" if result else "No suitable tee times found"
        }

        logger.info(f"Booking automation completed: {last_booking_result['message']}")

    except Exception as e:
        error_msg = f"Error during booking automation: {str(e)}"
        logger.error(error_msg)
        last_booking_result = {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "message": error_msg
        }
    finally:
        booking_in_progress = False
        loop.close()

@app.route('/')
def home():
    """Home page with basic info"""
    return jsonify({
        "service": "Tee Time Booking Automation",
        "status": "online",
        "endpoints": {
            "/run": "Trigger tee time booking",
            "/status": "Check booking status",
            "/health": "Health check"
        },
        "last_booking": last_booking_result
    })

@app.route('/run', methods=['GET', 'POST'])
def run_booking():
    """Trigger the tee time booking automation"""
    global booking_in_progress

    if booking_in_progress:
        return jsonify({
            "status": "already_running",
            "message": "Booking automation is already in progress",
            "timestamp": datetime.now().isoformat()
        }), 429

    # Get optional parameters
    test_mode = request.args.get('test', 'false').lower() == 'true'

    if test_mode:
        return jsonify({
            "status": "test_success",
            "message": "Test mode - booking automation would run here",
            "timestamp": datetime.now().isoformat(),
            "next_booking_date": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        })

    # Start booking in background thread
    booking_thread = threading.Thread(target=run_booking_async)
    booking_thread.daemon = True
    booking_thread.start()

    return jsonify({
        "status": "started",
        "message": "Tee time booking automation started",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/status')
def get_status():
    """Check the status of the booking automation"""
    return jsonify({
        "booking_in_progress": booking_in_progress,
        "last_result": last_booking_result,
        "current_time": datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "tee-time-booking-automation",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=5000, debug=True)
