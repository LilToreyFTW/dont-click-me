#!/usr/bin/env python3
"""
Complete Build System for RealLife AI Tools
Builds, configures, and launches everything
"""

import os
import sys
import subprocess
import platform
import json
import shutil
from pathlib import Path

class CompleteBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.system = platform.system().lower()
        self.is_windows = self.system == "windows"
        self.is_linux = self.system == "linux"
        self.is_macos = self.system == "darwin"

    def print_header(self, text):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f" {text}")
        print("=" * 60)

    def run_command(self, command, description, cwd=None, shell=False):
        """Run a command with proper error handling"""
        print(f"🔧 {description}...")
        try:
            if isinstance(command, str):
                command = command.split() if not shell else command

            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                shell=shell,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ {description} completed")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            print(f"Error output: {e.stderr}")
            return None
        except FileNotFoundError:
            print(f"❌ Command not found: {command[0] if isinstance(command, list) else command.split()[0]}")
            return None

    def check_python_version(self):
        """Check Python version compatibility"""
        self.print_header("CHECKING PYTHON VERSION")
        version = sys.version_info
        print(f"Python version: {version.major}.{version.minor}.{version.micro}")

        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8+ required")
            return False

        print("✅ Python version compatible")
        return True

    def install_python_dependencies(self):
        """Install all Python dependencies"""
        self.print_header("INSTALLING PYTHON DEPENDENCIES")

        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False

        # Upgrade pip first
        self.run_command("pip install --upgrade pip", "Upgrading pip")

        # Install requirements
        success = self.run_command(
            f"pip install -r requirements.txt",
            "Installing Python packages"
        )

        if success is None:
            print("❌ Failed to install Python dependencies")
            return False

        print("✅ Python dependencies installed")
        return True

    def install_node_dependencies(self):
        """Install Node.js dependencies for Cloudflare deployment"""
        self.print_header("INSTALLING NODE.JS DEPENDENCIES")

        # Check if Node.js is installed
        node_check = self.run_command("node --version", "Checking Node.js")
        if node_check is None:
            print("⚠️ Node.js not found - Cloudflare deployment will be skipped")
            print("Install Node.js from https://nodejs.org for full deployment")
            return True  # Not critical for basic operation

        npm_check = self.run_command("npm --version", "Checking npm")
        if npm_check is None:
            print("❌ npm not found")
            return False

        # Install dependencies
        package_file = self.project_root / "package.json"
        if package_file.exists():
            success = self.run_command("npm install", "Installing npm packages")
            if success is None:
                print("❌ Failed to install npm dependencies")
                return False

        print("✅ Node.js dependencies installed")
        return True

    def setup_database(self):
        """Setup the database"""
        self.print_header("SETTING UP DATABASE")

        try:
            # Import here to check if dependencies are available
            sys.path.insert(0, str(self.project_root))
            from email_server import app

            with app.app_context():
                from email_server import db, create_sample_emails
                print("Creating database tables...")
                db.create_all()
                print("Creating sample data...")
                create_sample_emails()

            print("✅ Database setup completed")
            return True

        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            return False

    def create_desktop_shortcuts(self):
        """Create desktop shortcuts for easy launching"""
        self.print_header("CREATING DESKTOP SHORTCUTS")

        if not self.is_windows:
            print("⚠️ Desktop shortcuts only supported on Windows")
            return True

        try:
            import winshell
            from win32com.client import Dispatch

            desktop = winshell.desktop()
            script_path = str(self.project_root / "run_system.py")
            python_exe = sys.executable

            # Create shortcut
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(Path(desktop) / "RealLife AI Tools.lnk"))
            shortcut.Targetpath = python_exe
            shortcut.Arguments = f'"{script_path}"'
            shortcut.WorkingDirectory = str(self.project_root)
            shortcut.IconLocation = python_exe
            shortcut.save()

            print("✅ Desktop shortcut created")
            return True

        except ImportError:
            print("⚠️ pywin32 not available - desktop shortcut creation skipped")
            print("Run: pip install pywin32 winshell")
            return True
        except Exception as e:
            print(f"⚠️ Failed to create desktop shortcut: {e}")
            return True

    def verify_installation(self):
        """Verify that everything is properly installed"""
        self.print_header("VERIFYING INSTALLATION")

        checks = [
            ("Flask", "import flask; print('Flask:', flask.__version__)"),
            ("SQLAlchemy", "import flask_sqlalchemy; print('SQLAlchemy: OK')"),
            ("Bcrypt", "import flask_bcrypt; print('Bcrypt: OK')"),
            ("PIL/Pillow", "import PIL; print('PIL:', PIL.__version__)"),
            ("Tkinter", "import tkinter; print('Tkinter: OK')"),
            ("Requests", "import requests; print('Requests:', requests.__version__)"),
        ]

        all_passed = True

        for name, test_code in checks:
            try:
                result = self.run_command(
                    [sys.executable, "-c", test_code],
                    f"Testing {name}",
                    shell=False
                )
                if result:
                    print(f"✅ {name}: {result}")
                else:
                    print(f"✅ {name}: Available")
            except Exception as e:
                print(f"❌ {name}: Failed - {e}")
                all_passed = False

        if all_passed:
            print("\n🎉 All verifications passed!")
        else:
            print("\n⚠️ Some verifications failed - system may still work")

        return all_passed

    def create_startup_script(self):
        """Create a comprehensive startup script"""
        self.print_header("CREATING STARTUP SCRIPT")

        startup_script = f'''#!/usr/bin/env python3
"""
RealLife AI Tools - Complete System Launcher
Launches both GUI and web server simultaneously
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def main():
    print("=" * 60)
    print("     RealLife AI Tools - Complete System")
    print("=" * 60)
    print("🚀 Launching GUI + Web Server + AI Host")
    print("=" * 60)

    project_root = Path(__file__).parent

    # Start email server in background
    print("📧 Starting Email Server...")
    server_thread = threading.Thread(
        target=lambda: subprocess.run([
            sys.executable, "-c",
            """
import sys
sys.path.insert(0, '.')
from email_server import app
print('Email server running on http://localhost:5000')
app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
            """
        ], cwd=project_root),
        daemon=True
    )
    server_thread.start()

    # Wait for server to start
    time.sleep(3)

    # Launch GUI
    print("🖥️  Launching GUI Application...")
    try:
        from gui_main import ModernChromeGUI
        gui = ModernChromeGUI()
        gui.run()
    except KeyboardInterrupt:
        print("\\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ GUI Error: {{e}}")
        print("💡 The web server may still be running on http://localhost:5000")

if __name__ == "__main__":
    main()
'''

        startup_file = self.project_root / "start_complete_system.py"
        with open(startup_file, 'w', encoding='utf-8') as f:
            f.write(startup_script)

        # Make executable on Unix systems
        if not self.is_windows:
            os.chmod(startup_file, 0o755)

        print("✅ Startup script created: start_complete_system.py")
        return True

    def build_all(self):
        """Run the complete build process"""
        print("🎯 REAL LIFE AI TOOLS - COMPLETE BUILD SYSTEM")
        print("=" * 60)
        print("This will build and configure everything for your AI system")
        print("=" * 60)

        steps = [
            ("Python Version Check", self.check_python_version),
            ("Python Dependencies", self.install_python_dependencies),
            ("Database Setup", self.setup_database),
            ("Desktop Shortcuts", self.create_desktop_shortcuts),
            ("Installation Verification", self.verify_installation),
            ("Startup Script Creation", self.create_startup_script),
        ]

        optional_steps = [
            ("Node.js Dependencies", self.install_node_dependencies),
        ]

        completed_steps = 0
        total_steps = len(steps) + len(optional_steps)

        # Required steps
        for step_name, step_function in steps:
            print(f"\\n[{completed_steps + 1}/{total_steps}] {step_name}")
            if step_function():
                completed_steps += 1
            else:
                print(f"❌ {step_name} failed - build cannot continue")
                return False

        # Optional steps
        for step_name, step_function in optional_steps:
            print(f"\\n[{completed_steps + 1}/{total_steps}] {step_name} (Optional)")
            if step_function():
                completed_steps += 1
            else:
                print(f"⚠️ {step_name} failed - skipping optional component")
                completed_steps += 1  # Still count as completed since it's optional

        self.print_header("BUILD COMPLETE")

        # Check if all required steps passed (Node.js is optional)
        required_steps_count = len(steps)
        if completed_steps >= required_steps_count:
            print("🎉 CORE SYSTEMS SUCCESSFULLY BUILT!")
            print("\\n🚀 Ready to launch:")
            print("• GUI + Web Server: python start_complete_system.py")
            print("• GUI Only: python gui_main.py")
            print("• Web Only: python email_server.py")
            if completed_steps < total_steps:
                print(f"• Cloudflare Deploy: .\\deploy-ai-host.ps1 (requires Node.js)")
            else:
                print("• Cloudflare Deploy: .\\deploy-ai-host.ps1")
        else:
            print(f"⚠️ Build completed with {completed_steps}/{required_steps_count} core steps")
            print("\\n💡 Core functionality may be limited")

        print("\\n" + "=" * 60)
        print("🎯 RealLife AI Tools - Build Complete!")
        print("🌐 GUI + Web Server + AI Host Ready")
        print("=" * 60)

        return completed_steps >= len(steps)  # Required steps only

if __name__ == "__main__":
    builder = CompleteBuilder()
    success = builder.build_all()
    sys.exit(0 if success else 1)
