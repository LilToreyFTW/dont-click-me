#!/usr/bin/env python3
"""
RealLife AI Tools Launcher
Runs both the GUI interface and email server
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_bcrypt
        import flask_mail
        import PIL
        import tkinter
        print("[OK] All required packages are installed")
        return True
    except ImportError as e:
        print(f"[ERROR] Missing required package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def start_email_server():
    """Start the email server in a separate thread"""
    try:
        print("Starting email server...")
        # Import here to avoid issues if dependencies are missing
        from email_server import app

        # Run in a separate thread
        def run_server():
            app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait a moment for server to start
        time.sleep(2)
        print("[OK] Email server started on http://localhost:5000")

        # Open browser to email server
        webbrowser.open("http://localhost:5000")

        return True
    except Exception as e:
        print(f"[ERROR] Failed to start email server: {e}")
        return False

def start_gui():
    """Start the GUI application"""
    try:
        print("Starting GUI application...")
        from gui_main import ModernChromeGUI

        gui = ModernChromeGUI()
        gui.run()
    except Exception as e:
        print(f"✗ Failed to start GUI: {e}")

def main():
    """Main launcher function"""
    print("=" * 60)
    print("     RealLife AI Tools - Discord Account Manager")
    print("=" * 60)
    print("Features:")
    print("• Modern Chrome-style GUI (1920x1080)")
    print("• Integrated Brave Browser")
    print("• Email server with user management")
    print("• Professional email interface")
    print("=" * 60)

    # Check if we're in the right directory
    if not Path("gui_main.py").exists() or not Path("email_server.py").exists():
        print("✗ Error: Please run this script from the DiscordAccount-making directory")
        sys.exit(1)

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Start email server first
    if start_email_server():
        print("\n" + "=" * 60)
        print("Ready! Starting GUI in 3 seconds...")
        print("The email server is running at: http://localhost:5000")
        print("=" * 60)

        time.sleep(3)

        # Start GUI (this will block until GUI is closed)
        start_gui()
    else:
        print("Failed to start email server. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
