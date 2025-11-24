#!/usr/bin/env python3
"""
System Status Checker for RealLife AI Tools
Verifies that both GUI and web server are working properly
"""

import sys
import requests
import subprocess
import time
import socket
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def check_port_open(host, port):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_web_server():
    """Check if the web server is running and responding"""
    print_header("WEB SERVER STATUS")

    # Check if port 5000 is open
    if not check_port_open('localhost', 5000):
        print("❌ Web server port 5000 is not accessible")
        print("💡 Start the web server with: python email_server.py")
        return False

    print("✅ Web server port 5000 is open")

    # Check health endpoint
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   Version: {health_data.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Health check failed: {e}")
        print("💡 Make sure the web server is running")
        return False

def check_gui_imports():
    """Check if GUI components can be imported"""
    print_header("GUI COMPONENT CHECK")

    try:
        # Test basic imports
        import tkinter
        print("✅ Tkinter available")

        import PIL
        print("✅ PIL/Pillow available")

        # Test GUI-specific imports
        from gui_main import ModernChromeGUI, EmbeddedDiscordBrowser
        print("✅ GUI classes can be imported")

        # Test email server import
        from email_server import app
        print("✅ Email server can be imported")

        print("✅ All GUI components ready")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ GUI check failed: {e}")
        return False

def check_database():
    """Check database connectivity"""
    print_header("DATABASE STATUS")

    try:
        from email_server import app, db
        with app.app_context():
            # Try to query the database
            from email_server import User, EmailMessage
            user_count = User.query.count()
            email_count = EmailMessage.query.count()

            print("✅ Database connection successful")
            print(f"   Users: {user_count}")
            print(f"   Emails: {email_count}")
            return True

    except Exception as e:
        print(f"❌ Database error: {e}")
        print("💡 The database will be created when you first run the system")
        return False

def check_api_endpoints():
    """Check various API endpoints"""
    print_header("API ENDPOINT CHECK")

    endpoints = [
        ("Home", "/"),
        ("Health", "/health"),
        ("Register", "/register"),
        ("Login", "/login"),
        ("Dashboard", "/dashboard"),
    ]

    working_endpoints = 0

    for name, endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=5)
            if response.status_code in [200, 302]:  # 302 is redirect, which is OK
                print(f"✅ {name} ({endpoint}): {response.status_code}")
                working_endpoints += 1
            else:
                print(f"⚠️  {name} ({endpoint}): {response.status_code}")
        except requests.RequestException:
            print(f"❌ {name} ({endpoint}): Not accessible")

    if working_endpoints == len(endpoints):
        print("✅ All API endpoints working")
        return True
    else:
        print(f"⚠️  {working_endpoints}/{len(endpoints)} endpoints working")
        return working_endpoints > 0

def check_file_structure():
    """Check if all required files are present"""
    print_header("FILE STRUCTURE CHECK")

    required_files = [
        "gui_main.py",
        "email_server.py",
        "run_system.py",
        "unified_launcher.py",
        "build_all.py",
        "requirements.txt",
        "templates/index.html",
        "templates/login.html",
        "templates/register.html",
        "templates/dashboard.html",
        "static/css/style.css",
        "static/js/main.js"
    ]

    project_root = Path(__file__).parent
    missing_files = []

    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)

    if not missing_files:
        print("✅ All required files present")
        return True
    else:
        print(f"❌ {len(missing_files)} files missing")
        return False

def run_full_system_test():
    """Run a comprehensive system test"""
    print_header("COMPLETE SYSTEM TEST")

    tests = [
        ("File Structure", check_file_structure),
        ("GUI Components", check_gui_imports),
        ("Web Server", check_web_server),
        ("Database", check_database),
        ("API Endpoints", check_api_endpoints),
    ]

    passed_tests = 0
    total_tests = len(tests)

    for test_name, test_function in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_function():
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")

    print_header("TEST RESULTS")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is fully operational")
        print("\n🚀 Ready to launch:")
        print("• Complete System: python unified_launcher.py")
        print("• GUI Only: python gui_main.py")
        print("• Web Only: python email_server.py")
        return True
    else:
        print(f"⚠️ {passed_tests}/{total_tests} tests passed")
        print("\n💡 To fix issues:")
        print("• Run: python build_all.py (to install dependencies)")
        print("• Start web server: python email_server.py")
        print("• Then run this check again")

        if passed_tests >= total_tests * 0.8:  # 80% pass rate
            print("\n🟡 System mostly ready - some features may not work")
        else:
            print("\n❌ System needs attention before use")

        return False

def main():
    """Main function"""
    print("🔍 REAL LIFE AI TOOLS - SYSTEM STATUS CHECKER")
    print("=" * 60)
    print("This will verify that your complete AI system is working properly")
    print("=" * 60)

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick check - just verify basic functionality
        success = check_file_structure() and check_gui_imports()
        if success:
            print("\n✅ Quick check passed - System ready!")
        else:
            print("\n❌ Quick check failed - Run full build")
        return 0 if success else 1

    # Full system test
    success = run_full_system_test()

    print("\n" + "=" * 60)
    print("🔍 System Check Complete")
    print("=" * 60)

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
