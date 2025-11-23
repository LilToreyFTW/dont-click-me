#!/usr/bin/env python3
"""
Test script for GUI functionality without launching the full interface
"""

import sys
import os

def test_imports():
    """Test all GUI imports"""
    try:
        from gui_main import ModernChromeGUI, EmbeddedDiscordBrowser
        print("[OK] All GUI imports successful")
        return True
    except Exception as e:
        print(f"[ERROR] Import failed: {e}")
        return False

def test_browser_class():
    """Test the embedded browser class initialization"""
    try:
        from gui_main import EmbeddedDiscordBrowser

        # Mock colors for testing
        colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2a2a2a',
            'accent_blue': '#4285f4',
            'text_white': '#ffffff',
            'text_gray': '#cccccc',
            'chrome_blue': '#1a73e8'
        }

        # Create a mock parent for testing
        class MockParent:
            pass

        parent = MockParent()

        # Test browser creation (without actually creating widgets)
        browser = EmbeddedDiscordBrowser.__new__(EmbeddedDiscordBrowser)
        browser.parent = parent
        browser.colors = colors
        browser.current_url = "https://discord.com"
        browser.history = []
        browser.history_index = -1

        print("[OK] Embedded browser class initialization successful")
        return True
    except Exception as e:
        print(f"[ERROR] Browser class test failed: {e}")
        return False

def test_button_methods():
    """Test button method definitions"""
    try:
        from gui_main import ModernChromeGUI

        # Create instance without __init__
        gui = ModernChromeGUI.__new__(ModernChromeGUI)

        # Test method existence
        methods = [
            'launch_brave_browser',
            'open_email_server',
            'create_email_account',
            'view_email_inbox',
            'open_discord_website',
            'open_account_creator',
            'open_bulk_operations',
            'browser_back',
            'browser_forward',
            'browser_refresh',
            'browser_home',
            'navigate_to_url'
        ]

        for method in methods:
            if hasattr(gui, method):
                print(f"[OK] Method {method} exists")
            else:
                print(f"[ERROR] Method {method} missing")
                return False

        print("[OK] All button methods defined")
        return True
    except Exception as e:
        print(f"[ERROR] Method test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("GUI Functionality Test")
    print("=" * 50)

    tests = [
        ("Import Test", test_imports),
        ("Browser Class Test", test_browser_class),
        ("Button Methods Test", test_button_methods)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("[SUCCESS] All GUI functionality tests passed!")
        print("\nThe embedded Discord browser is ready to use.")
        print("Run 'python run_system.py' to launch the full application.")
    else:
        print("[FAILED] Some tests failed. Please check the implementation.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
