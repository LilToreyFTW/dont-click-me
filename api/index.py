"""
Vercel-compatible Flask application entry point for RealLife AI Email System
"""

from flask import Flask
import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Import the email server application
from email_server import app

# Vercel expects the Flask app to be named 'app'
# But we already have it imported as 'app' from email_server

# For Vercel, we need to export the app
app = app

if __name__ == "__main__":
    app.run(debug=True)
