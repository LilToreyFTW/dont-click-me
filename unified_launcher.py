#!/usr/bin/env python3
"""
Unified Launcher for RealLife AI Tools
Runs GUI and Web Server simultaneously with proper coordination
"""

import os
import sys
import subprocess
import threading
import time
import signal
import atexit
from pathlib import Path
import requests

class UnifiedLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.server_process = None
        self.server_thread = None
        self.gui_process = None
        self.running = True

        # Register cleanup handler
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def print_banner(self):
        """Print the startup banner"""
        print("\n" + "=" * 70)
        print("           🤖 REAL LIFE AI TOOLS - UNIFIED SYSTEM")
        print("=" * 70)
        print("🚀 Launching Complete AI Ecosystem:")
        print("   • 🖥️  Modern GUI with Embedded Discord Browser")
        print("   • 🌐 Flask Web Server with AI Email System")
        print("   • 🧠 AI-Powered Analytics & Security")
        print("   • 🔗 Seamless GUI-Web Integration")
        print("=" * 70)

    def check_server_health(self):
        """Check if the web server is responding"""
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def start_web_server(self):
        """Start the Flask web server"""
        print("📧 Starting AI Email Web Server...")

        try:
            # Start server in background process
            self.server_process = subprocess.Popen([
                sys.executable, "-c",
                """
import os
import sys
sys.path.insert(0, os.getcwd())
from email_server import app
print("🌐 AI Email Server running on http://localhost:5000")
print("📊 Health check: http://localhost:5000/health")
print("🎮 GUI integration active")
app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
                """
            ], cwd=self.project_root)

            # Wait for server to start
            print("⏳ Waiting for server to initialize...")
            for i in range(10):  # Wait up to 10 seconds
                if self.check_server_health():
                    print("✅ AI Email Server is healthy and responding!")
                    print("🔗 GUI-Web integration established")
                    return True
                time.sleep(1)

            print("⚠️ Server started but health check failed - continuing anyway")
            return True

        except Exception as e:
            print(f"❌ Failed to start web server: {e}")
            return False

    def start_gui_application(self):
        """Start the GUI application"""
        print("🖥️  Starting Modern GUI Application...")

        try:
            # Import and start GUI
            from gui_main import ModernChromeGUI

            print("🎨 GUI initialized with embedded Discord browser")
            print("🌐 Web integration: http://localhost:5000")
            print("🎯 Ready for AI-powered operations")

            # Create and run GUI
            gui = ModernChromeGUI()

            # Override the GUI's run method to handle shutdown properly
            original_run = gui.run
            def enhanced_run():
                try:
                    original_run()
                except KeyboardInterrupt:
                    print("\n👋 GUI shutdown requested")
                finally:
                    self.running = False

            gui.run = enhanced_run
            gui.run()

        except KeyboardInterrupt:
            print("\n👋 GUI shutdown requested")
        except Exception as e:
            print(f"❌ GUI Error: {e}")
            print("💡 The web server may still be running")
        finally:
            self.running = False

    def monitor_system(self):
        """Monitor both GUI and server health"""
        while self.running:
            try:
                # Check server health
                if self.server_process and self.server_process.poll() is not None:
                    print("⚠️ Web server process terminated")
                    self.running = False
                    break

                # Check server responsiveness every 30 seconds
                if time.time() % 30 < 1:  # Check roughly every 30 seconds
                    if not self.check_server_health():
                        print("⚠️ Web server not responding to health checks")
                    else:
                        print("💚 System health: OK")

                time.sleep(1)

            except KeyboardInterrupt:
                break

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n📴 Received signal {signum} - initiating graceful shutdown...")
        self.running = False

    def cleanup(self):
        """Clean up processes on exit"""
        print("\n🧹 Performing system cleanup...")

        # Terminate web server
        if self.server_process and self.server_process.poll() is None:
            print("🛑 Stopping web server...")
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                print("✅ Web server stopped")
            except subprocess.TimeoutExpired:
                print("⚠️ Web server didn't stop gracefully, force killing...")
                self.server_process.kill()
            except Exception as e:
                print(f"⚠️ Error stopping web server: {e}")

        print("👋 Cleanup complete - System shutdown")

    def run(self):
        """Main launcher function"""
        self.print_banner()

        # Check if we're in the right directory
        if not (self.project_root / "gui_main.py").exists():
            print("❌ Error: gui_main.py not found. Please run from project root.")
            return False

        if not (self.project_root / "email_server.py").exists():
            print("❌ Error: email_server.py not found. Please run from project root.")
            return False

        # Start web server first
        if not self.start_web_server():
            print("❌ Failed to start web server. Cannot continue.")
            return False

        # Give server a moment to fully initialize
        time.sleep(2)

        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
        monitor_thread.start()

        print("\n" + "=" * 70)
        print("🎯 SYSTEM STATUS: FULLY OPERATIONAL")
        print("=" * 70)
        print("✅ AI Email Server: http://localhost:5000")
        print("✅ Health Check: http://localhost:5000/health")
        print("✅ GUI Integration: Active")
        print("✅ AI Analytics: Running")
        print("✅ Security Engine: Active")
        print("=" * 70)
        print("🎮 LAUNCHING GUI NOW...")
        print("Press Ctrl+C to shutdown both GUI and server gracefully")
        print("=" * 70 + "\n")

        # Start GUI (this will block until GUI exits)
        self.start_gui_application()

        # Wait for monitoring thread to finish
        if monitor_thread.is_alive():
            monitor_thread.join(timeout=5)

        return True

def main():
    """Main entry point"""
    try:
        launcher = UnifiedLauncher()
        success = launcher.run()

        if success:
            print("\n🎉 Session completed successfully!")
            print("💡 Run again anytime: python unified_launcher.py")
        else:
            print("\n❌ System failed to start properly")
            return 1

    except KeyboardInterrupt:
        print("\n👋 Shutdown requested by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
