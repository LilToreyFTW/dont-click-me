"""
Vercel-compatible Flask application entry point for RealLife AI Email System
"""

import os
import sys

# Add the parent directory to Python path for imports
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    # Import the email server application
    from email_server import app
    print("Successfully imported Flask app")
except Exception as e:
    print(f"Import error: {e}")
    # Create a minimal app for debugging
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def home():
        return f"Import Error: {e}"

    @app.route('/debug')
    def debug():
        return {
            "error": str(e),
            "python_path": sys.path,
            "current_dir": current_dir,
            "parent_dir": parent_dir
        }

# This is what Vercel looks for - the WSGI application
application = app

if __name__ == "__main__":
    # For local testing
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
