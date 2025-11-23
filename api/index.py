"""
Vercel-compatible Flask application entry point for RealLife AI Email System
"""

import os
import sys

# Add the parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the email server application
from email_server import app

# Vercel serverless function handler
def handler(request, context):
    """
    Vercel serverless function handler for Flask app
    """
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from werkzeug.serving import WSGIRequestHandler

    # Return the Flask WSGI app
    return app

# Export the app for Vercel (this is what Vercel looks for)
app = app

if __name__ == "__main__":
    # For local testing
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
