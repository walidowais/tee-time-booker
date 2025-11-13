#!/usr/bin/env python3
"""
Simple test server to verify Replit is working
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "working",
        "message": "Replit server is running!",
        "service": "tee-time-booking"
    })

@app.route('/test')
def test():
    return jsonify({
        "test": "success",
        "message": "Basic Flask app is working"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
