#!/usr/bin/env python3
"""
Modern GUI Interface for Discord Account Management
Features: 1920x1080 resolution, Chrome blue/black/white theme, Embedded Discord browser
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import subprocess
import sys
import os
import webbrowser
import threading
import time
from PIL import Image, ImageTk
import requests
from io import BytesIO
from urllib.parse import urlparse, urljoin
import json
import re

class EmbeddedDiscordBrowser:
    """Custom embedded browser for Discord operations within the GUI"""

    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        self.current_url = "https://discord.com"
        self.history = []
        self.history_index = -1
        self.cookies = {}
        self.session = requests.Session()

        # Create browser UI
        self.create_browser_ui()

    def create_browser_ui(self):
        """Create the browser interface"""
        # Browser container
        self.browser_frame = tk.Frame(self.parent, bg=self.colors['bg_medium'])

        # Navigation bar
        self.create_navigation_bar()

        # Content area
        self.create_content_area()

        # Status bar
        self.create_browser_status_bar()

    def create_navigation_bar(self):
        """Create browser navigation bar"""
        nav_frame = tk.Frame(self.browser_frame, bg=self.colors['bg_dark'], height=50)
        nav_frame.pack(fill=tk.X, pady=(0, 5))
        nav_frame.pack_propagate(False)

        # Navigation buttons
        button_frame = tk.Frame(nav_frame, bg=self.colors['bg_dark'])
        button_frame.pack(side=tk.LEFT, padx=10)

        nav_buttons = [
            ("←", self.go_back, "Back"),
            ("→", self.go_forward, "Forward"),
            ("🔄", self.refresh, "Refresh"),
            ("🏠", self.go_home, "Home")
        ]

        self.nav_buttons = {}
        for symbol, cmd, tooltip in nav_buttons:
            btn = tk.Button(button_frame, text=symbol,
                           font=('Segoe UI', 12),
                           bg=self.colors['bg_dark'],
                           fg=self.colors['text_white'],
                           borderwidth=0,
                           padx=8, pady=5,
                           command=cmd)
            btn.pack(side=tk.LEFT, padx=(0, 5))
            btn.bind("<Enter>", lambda e, t=tooltip: self.show_tooltip(t))
            btn.bind("<Leave>", lambda e: self.hide_tooltip())
            self.nav_buttons[tooltip.lower()] = btn

        # URL bar
        url_frame = tk.Frame(nav_frame, bg=self.colors['bg_dark'])
        url_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))

        url_label = tk.Label(url_frame, text="🔒",
                            font=('Segoe UI', 10),
                            fg=self.colors['text_white'],
                            bg=self.colors['bg_dark'])
        url_label.pack(side=tk.LEFT, padx=(0, 5))

        self.url_entry = tk.Entry(url_frame,
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_light'],
                                 fg=self.colors['text_white'],
                                 insertbackground=self.colors['text_white'],
                                 borderwidth=0,
                                 relief=tk.FLAT)
        self.url_entry.pack(fill=tk.X, expand=True, pady=8)
        self.url_entry.insert(0, self.current_url)
        self.url_entry.bind("<Return>", self.navigate_to_url)

        go_btn = tk.Button(url_frame, text="Go",
                          font=('Segoe UI', 10, 'bold'),
                          bg=self.colors['chrome_blue'],
                          fg=self.colors['text_white'],
                          borderwidth=0,
                          padx=15, pady=5,
                          command=self.navigate_to_url)
        go_btn.pack(side=tk.RIGHT, padx=(10, 0))

    def create_content_area(self):
        """Create the main content display area"""
        content_frame = tk.Frame(self.browser_frame, bg=self.colors['bg_light'])
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Create a scrolled text widget for content display
        self.content_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg=self.colors['bg_dark'],
            fg=self.colors['text_white'],
            insertbackground=self.colors['text_white'],
            selectbackground=self.colors['chrome_blue'],
            selectforeground=self.colors['text_white'],
            borderwidth=0,
            padx=10, pady=10
        )

        # Configure tags for different content types
        self.content_text.tag_configure("title", font=('Segoe UI', 16, 'bold'), foreground=self.colors['chrome_blue'])
        self.content_text.tag_configure("heading", font=('Segoe UI', 14, 'bold'), foreground=self.colors['text_white'])
        self.content_text.tag_configure("link", foreground=self.colors['chrome_blue'], underline=True)
        self.content_text.tag_configure("button", background=self.colors['chrome_blue'], foreground=self.colors['text_white'], relief=tk.RAISED)
        self.content_text.tag_configure("input", background=self.colors['bg_light'], foreground=self.colors['text_white'])

        self.content_text.pack(fill=tk.BOTH, expand=True)

        # Bind link clicking
        self.content_text.tag_bind("link", "<Button-1>", self.handle_link_click)
        self.content_text.tag_bind("link", "<Enter>", lambda e: self.content_text.config(cursor="hand2"))
        self.content_text.tag_bind("link", "<Leave>", lambda e: self.content_text.config(cursor=""))

        # Initial Discord page load
        self.load_discord_page()

    def create_browser_status_bar(self):
        """Create browser status bar"""
        self.browser_status_frame = tk.Frame(self.browser_frame, bg=self.colors['bg_dark'], height=25)
        self.browser_status_frame.pack(fill=tk.X)
        self.browser_status_frame.pack_propagate(False)

        self.browser_status_label = tk.Label(
            self.browser_status_frame,
            text="Ready - Discord Browser",
            font=('Segoe UI', 8),
            fg=self.colors['text_gray'],
            bg=self.colors['bg_dark'],
            anchor='w'
        )
        self.browser_status_label.pack(fill=tk.X, padx=10)

    def load_discord_page(self, url=None):
        """Load Discord page content"""
        if url:
            self.current_url = url
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)

        # Add to history
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history.append(self.current_url)
        self.history_index = len(self.history) - 1

        # Update navigation buttons
        self.update_nav_buttons()

        # Load Discord-specific content
        self.display_discord_content()

    def display_discord_content(self):
        """Display Discord-specific content in the browser"""
        self.content_text.delete(1.0, tk.END)

        if "discord.com" in self.current_url:
            if "/login" in self.current_url or self.current_url.endswith("discord.com"):
                self.display_discord_login()
            elif "/register" in self.current_url:
                self.display_discord_register()
            elif "/app" in self.current_url:
                self.display_discord_app()
            else:
                self.display_discord_home()
        else:
            self.display_external_page()

    def display_discord_home(self):
        """Display Discord home page"""
        content = """Discord - Free Voice and Text Chat for Gamers

Welcome to Discord!

Discord is the easiest way to communicate over voice, video, and text. Chat, hang out, and stay close with your friends and communities.

"""

        self.content_text.insert(tk.END, "Discord\n", "title")
        self.content_text.insert(tk.END, "=" * 50 + "\n\n")

        self.content_text.insert(tk.END, "🎮 Free Voice and Text Chat for Gamers\n\n", "heading")

        self.content_text.insert(tk.END, "Discord is the easiest way to communicate over voice, video, and text. ")
        self.content_text.insert(tk.END, "Chat, hang out, and stay close with your friends and communities.\n\n")

        # Login button
        self.content_text.insert(tk.END, "[ LOGIN ]", "button")
        self.content_text.insert(tk.END, " ")
        self.content_text.insert(tk.END, "[ REGISTER ]", "button")
        self.content_text.insert(tk.END, "\n\n")

        # Features
        self.content_text.insert(tk.END, "✨ Features:\n", "heading")
        self.content_text.insert(tk.END, "• Create servers for your communities\n")
        self.content_text.insert(tk.END, "• Voice channels for talking\n")
        self.content_text.insert(tk.END, "• Text channels for messaging\n")
        self.content_text.insert(tk.END, "• Screen sharing and video calls\n")
        self.content_text.insert(tk.END, "• Custom emojis and roles\n")
        self.content_text.insert(tk.END, "• Bot integrations\n\n")

        self.content_text.insert(tk.END, "📱 Available on: Windows, macOS, Linux, iOS, Android, Web\n\n")

        self.content_text.insert(tk.END, "🌐 ")
        self.content_text.insert(tk.END, "Download Discord", "link")
        self.content_text.insert(tk.END, " | ")
        self.content_text.insert(tk.END, "Open in Browser", "link")
        self.content_text.insert(tk.END, "\n\n")

        # Tag bindings for buttons
        self.content_text.tag_bind("button", "<Button-1>", self.handle_button_click)

    def display_discord_login(self):
        """Display Discord login page"""
        self.content_text.insert(tk.END, "Discord - Login\n", "title")
        self.content_text.insert(tk.END, "=" * 30 + "\n\n")

        self.content_text.insert(tk.END, "Welcome back!\n\n", "heading")

        self.content_text.insert(tk.END, "Email: ____________________\n")
        self.content_text.insert(tk.END, "Password: _________________\n\n")

        self.content_text.insert(tk.END, "[ LOGIN ]", "button")
        self.content_text.insert(tk.END, " ")
        self.content_text.insert(tk.END, "[ Forgot Password? ]", "link")
        self.content_text.insert(tk.END, "\n\n")

        self.content_text.insert(tk.END, "New to Discord? ")
        self.content_text.insert(tk.END, "Register here", "link")
        self.content_text.insert(tk.END, "\n\n")

        # QR Code login option
        self.content_text.insert(tk.END, "📱 Or login with QR code\n")
        self.content_text.insert(tk.END, "[📷 Scan QR Code]", "button")

        self.content_text.tag_bind("button", "<Button-1>", self.handle_login_button_click)

    def display_discord_register(self):
        """Display Discord registration page"""
        self.content_text.insert(tk.END, "Discord - Create Account\n", "title")
        self.content_text.insert(tk.END, "=" * 35 + "\n\n")

        self.content_text.insert(tk.END, "Create your Discord account\n\n", "heading")

        self.content_text.insert(tk.END, "Email: ____________________\n")
        self.content_text.insert(tk.END, "Username: _________________\n")
        self.content_text.insert(tk.END, "Password: _________________\n")
        self.content_text.insert(tk.END, "Date of Birth: __/__/____\n\n")

        self.content_text.insert(tk.END, "[ CONTINUE ]", "button")
        self.content_text.insert(tk.END, "\n\n")

        self.content_text.insert(tk.END, "By registering, you agree to Discord's ")
        self.content_text.insert(tk.END, "Terms of Service", "link")
        self.content_text.insert(tk.END, " and ")
        self.content_text.insert(tk.END, "Privacy Policy", "link")
        self.content_text.insert(tk.END, "\n\n")

        self.content_text.insert(tk.END, "Already have an account? ")
        self.content_text.insert(tk.END, "Login here", "link")

        self.content_text.tag_bind("button", "<Button-1>", self.handle_register_button_click)

    def display_discord_app(self):
        """Display Discord app interface"""
        self.content_text.insert(tk.END, "Discord - App\n", "title")
        self.content_text.insert(tk.END, "=" * 20 + "\n\n")

        self.content_text.insert(tk.END, "⚠️ Note: This is a simulated Discord interface.\n")
        self.content_text.insert(tk.END, "For full Discord functionality, please use the official Discord application.\n\n")

        # Server list
        self.content_text.insert(tk.END, "📋 Servers:\n", "heading")
        servers = ["My Server", "Gaming Hub", "Study Group", "Music Lounge"]
        for server in servers:
            self.content_text.insert(tk.END, f"• {server}\n")

        self.content_text.insert(tk.END, "\n💬 Channels:\n", "heading")
        channels = ["# general", "# gaming", "# music", "# memes"]
        for channel in channels:
            self.content_text.insert(tk.END, f"• {channel}\n")

        self.content_text.insert(tk.END, "\n👥 Online Users:\n", "heading")
        users = ["User1 (Online)", "User2 (Online)", "User3 (Away)", "User4 (Offline)"]
        for user in users:
            self.content_text.insert(tk.END, f"• {user}\n")

    def display_external_page(self):
        """Display external page warning"""
        self.content_text.insert(tk.END, "🔒 External Link\n", "title")
        self.content_text.insert(tk.END, "=" * 20 + "\n\n")

        self.content_text.insert(tk.END, f"URL: {self.current_url}\n\n")
        self.content_text.insert(tk.END, "⚠️ This embedded browser is optimized for Discord.\n")
        self.content_text.insert(tk.END, "For full web browsing, use your external browser.\n\n")

        self.content_text.insert(tk.END, "[ Open in External Browser ]", "button")
        self.content_text.insert(tk.END, " ")
        self.content_text.insert(tk.END, "[ Back to Discord ]", "button")

        self.content_text.tag_bind("button", "<Button-1>", self.handle_external_button_click)

    def handle_link_click(self, event):
        """Handle link clicking"""
        # Get the clicked text
        index = self.content_text.index(f"@{event.x},{event.y}")
        line_start = self.content_text.index(f"{index} linestart")
        line_end = self.content_text.index(f"{index} lineend")
        line_text = self.content_text.get(line_start, line_end)

        if "Download Discord" in line_text:
            self.load_discord_page("https://discord.com/download")
        elif "Open in Browser" in line_text:
            webbrowser.open(self.current_url)
        elif "Register here" in line_text:
            self.load_discord_page("https://discord.com/register")
        elif "Login here" in line_text:
            self.load_discord_page("https://discord.com/login")
        elif "Terms of Service" in line_text:
            self.load_discord_page("https://discord.com/terms")
        elif "Privacy Policy" in line_text:
            self.load_discord_page("https://discord.com/privacy")
        elif "Forgot Password?" in line_text:
            self.load_discord_page("https://discord.com/forgot")

    def handle_button_click(self, event):
        """Handle button clicking"""
        index = self.content_text.index(f"@{event.x},{event.y}")
        line_start = self.content_text.index(f"{index} linestart")
        line_end = self.content_text.index(f"{index} lineend")
        clicked_text = self.content_text.get(line_start, line_end)

        if "[ LOGIN ]" in clicked_text:
            self.load_discord_page("https://discord.com/login")
        elif "[ REGISTER ]" in clicked_text:
            self.load_discord_page("https://discord.com/register")

    def handle_login_button_click(self, event):
        """Handle login-specific buttons"""
        index = self.content_text.index(f"@{event.x},{event.y}")
        line_start = self.content_text.index(f"{index} linestart")
        line_end = self.content_text.index(f"{index} lineend")
        clicked_text = self.content_text.get(line_start, line_end)

        if "[ LOGIN ]" in clicked_text:
            messagebox.showinfo("Discord Login", "Login functionality would connect to Discord API here.")
            self.load_discord_page("https://discord.com/app")
        elif "[📷 Scan QR Code]" in clicked_text:
            messagebox.showinfo("QR Login", "QR code scanning would open camera here.")

    def handle_register_button_click(self, event):
        """Handle register-specific buttons"""
        index = self.content_text.index(f"@{event.x},{event.y}")
        line_start = self.content_text.index(f"{index} linestart")
        line_end = self.content_text.index(f"{index} lineend")
        clicked_text = self.content_text.get(line_start, line_end)

        if "[ CONTINUE ]" in clicked_text:
            messagebox.showinfo("Discord Registration", "Account creation would submit to Discord API here.")
            self.load_discord_page("https://discord.com/login")

    def handle_external_button_click(self, event):
        """Handle external page buttons"""
        index = self.content_text.index(f"@{event.x},{event.y}")
        line_start = self.content_text.index(f"{index} linestart")
        line_end = self.content_text.index(f"{index} lineend")
        clicked_text = self.content_text.get(line_start, line_end)

        if "[ Open in External Browser ]" in clicked_text:
            webbrowser.open(self.current_url)
        elif "[ Back to Discord ]" in clicked_text:
            self.load_discord_page("https://discord.com")

    def navigate_to_url(self, event=None):
        """Navigate to URL in address bar"""
        url = self.url_entry.get().strip()

        # Add https:// if not present
        if not url.startswith(('http://', 'https://')):
            if 'discord.com' in url or not '.' in url:
                url = 'https://discord.com/' + url.lstrip('/')
            else:
                url = 'https://' + url

        self.load_discord_page(url)

    def go_back(self):
        """Go back in history"""
        if self.history_index > 0:
            self.history_index -= 1
            self.load_discord_page(self.history[self.history_index])

    def go_forward(self):
        """Go forward in history"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.load_discord_page(self.history[self.history_index])

    def refresh(self):
        """Refresh current page"""
        self.display_discord_content()
        self.update_status("Page refreshed")

    def go_home(self):
        """Go to Discord home"""
        self.load_discord_page("https://discord.com")

    def update_nav_buttons(self):
        """Update navigation button states"""
        # Back button
        if self.history_index > 0:
            self.nav_buttons['back'].config(state=tk.NORMAL)
        else:
            self.nav_buttons['back'].config(state=tk.DISABLED)

        # Forward button
        if self.history_index < len(self.history) - 1:
            self.nav_buttons['forward'].config(state=tk.NORMAL)
        else:
            self.nav_buttons['forward'].config(state=tk.DISABLED)

    def update_status(self, message):
        """Update browser status"""
        self.browser_status_label.config(text=message)

    def show_tooltip(self, text):
        """Show tooltip"""
        self.browser_status_label.config(text=text)

    def hide_tooltip(self):
        """Hide tooltip"""
        self.browser_status_label.config(text="Ready - Discord Browser")

class ModernChromeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RealLife AI Tools - Discord Account Manager")
        self.root.geometry("1920x1080")
        self.root.configure(bg='#0a0a0a')

        # Chrome-style color scheme
        self.colors = {
            'bg_dark': '#0a0a0a',
            'bg_medium': '#1a1a1a',
            'bg_light': '#2a2a2a',
            'accent_blue': '#4285f4',
            'accent_blue_dark': '#3367d6',
            'text_white': '#ffffff',
            'text_gray': '#cccccc',
            'chrome_blue': '#1a73e8',
            'chrome_blue_hover': '#1557b0'
        }

        self.setup_styles()
        self.create_main_interface()
        self.embedded_browser = None
        self.brave_process = None

    def setup_styles(self):
        """Setup modern chrome-style ttk styles"""
        style = ttk.Style()

        # Configure overall theme
        style.configure('TFrame', background=self.colors['bg_dark'])
        style.configure('TLabel', background=self.colors['bg_dark'], foreground=self.colors['text_white'])
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))

        # Chrome-style button
        style.configure('Chrome.TButton',
                       background=self.colors['chrome_blue'],
                       foreground=self.colors['text_white'],
                       borderwidth=0,
                       focusthickness=0,
                       relief='flat',
                       padding=(20, 10))

        style.map('Chrome.TButton',
                 background=[('active', self.colors['chrome_blue_hover']),
                           ('pressed', self.colors['accent_blue_dark'])])

        # Modern card style
        style.configure('Card.TFrame',
                       background=self.colors['bg_medium'],
                       borderwidth=1,
                       relief='solid')

    def create_main_interface(self):
        """Create the main GUI interface"""
        # Main container
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header section with chrome styling
        self.create_header(main_frame)

        # Main content area
        content_frame = ttk.Frame(main_frame, style='TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(30, 0))

        # Left panel - Tools and controls
        left_panel = self.create_left_panel(content_frame)

        # Right panel - Browser integration
        right_panel = self.create_right_panel(content_frame)

        # Status bar
        self.create_status_bar(main_frame)

    def create_header(self, parent):
        """Create chrome-style header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_dark'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        # Logo/title area
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        title_frame.pack(side=tk.LEFT, padx=20)

        title_label = tk.Label(title_frame,
                              text="RealLife AI Tools",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['accent_blue'],
                              bg=self.colors['bg_dark'])
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_frame,
                                 text="Discord Account Management Suite",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['text_gray'],
                                 bg=self.colors['bg_dark'])
        subtitle_label.pack(anchor=tk.W)

        # Control buttons
        control_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        control_frame.pack(side=tk.RIGHT, padx=20)

        # Minimize button
        min_btn = tk.Button(control_frame, text="─", font=('Segoe UI', 12, 'bold'),
                           bg=self.colors['bg_dark'], fg=self.colors['text_white'],
                           borderwidth=0, command=self.minimize_window)
        min_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Close button
        close_btn = tk.Button(control_frame, text="✕", font=('Segoe UI', 12, 'bold'),
                             bg=self.colors['bg_dark'], fg=self.colors['text_white'],
                             borderwidth=0, command=self.root.quit)
        close_btn.pack(side=tk.LEFT)

    def create_left_panel(self, parent):
        """Create left control panel"""
        left_frame = tk.Frame(parent, bg=self.colors['bg_medium'], width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_frame.pack_propagate(False)

        # Tools section
        tools_label = tk.Label(left_frame, text="TOOLS & CONTROLS",
                              font=('Segoe UI', 14, 'bold'),
                              fg=self.colors['accent_blue'],
                              bg=self.colors['bg_medium'])
        tools_label.pack(pady=(20, 10), anchor=tk.W, padx=20)

        # Brave Browser section
        browser_frame = tk.Frame(left_frame, bg=self.colors['bg_light'])
        browser_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        browser_title = tk.Label(browser_frame, text="🌐 Brave Browser",
                                font=('Segoe UI', 12, 'bold'),
                                fg=self.colors['text_white'],
                                bg=self.colors['bg_light'])
        browser_title.pack(pady=(10, 5), anchor=tk.W, padx=10)

        launch_brave_btn = tk.Button(browser_frame, text="Launch Brave Browser",
                                    font=('Segoe UI', 10),
                                    bg=self.colors['chrome_blue'],
                                    fg=self.colors['text_white'],
                                    borderwidth=0,
                                    padx=20, pady=10,
                                    command=self.launch_brave_browser)
        launch_brave_btn.pack(pady=(0, 10), padx=10, fill=tk.X)

        # Email System section
        email_frame = tk.Frame(left_frame, bg=self.colors['bg_light'])
        email_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        email_title = tk.Label(email_frame, text="📧 Email System",
                              font=('Segoe UI', 12, 'bold'),
                              fg=self.colors['text_white'],
                              bg=self.colors['bg_light'])
        email_title.pack(pady=(10, 5), anchor=tk.W, padx=10)

        email_buttons = [
            ("Open Email Server", self.open_email_server),
            ("Create Account", self.create_email_account),
            ("View Inbox", self.view_email_inbox)
        ]

        for btn_text, cmd in email_buttons:
            btn = tk.Button(email_frame, text=btn_text,
                           font=('Segoe UI', 10),
                           bg=self.colors['bg_dark'],
                           fg=self.colors['text_white'],
                           borderwidth=0,
                           padx=20, pady=8,
                           command=cmd)
            btn.pack(pady=(0, 5), padx=10, fill=tk.X)

        # Discord Tools section
        discord_frame = tk.Frame(left_frame, bg=self.colors['bg_light'])
        discord_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        discord_title = tk.Label(discord_frame, text="🎮 Discord Tools",
                                font=('Segoe UI', 12, 'bold'),
                                fg=self.colors['text_white'],
                                bg=self.colors['bg_light'])
        discord_title.pack(pady=(10, 5), anchor=tk.W, padx=10)

        discord_buttons = [
            ("Go to Discord", self.open_discord_website),
            ("Account Creator", self.open_account_creator),
            ("Bulk Operations", self.open_bulk_operations)
        ]

        for btn_text, cmd in discord_buttons:
            btn = tk.Button(discord_frame, text=btn_text,
                           font=('Segoe UI', 10),
                           bg=self.colors['bg_dark'],
                           fg=self.colors['text_white'],
                           borderwidth=0,
                           padx=20, pady=8,
                           command=cmd)
            btn.pack(pady=(0, 5), padx=10, fill=tk.X)

        # System Status section
        status_frame = tk.Frame(left_frame, bg=self.colors['bg_light'])
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        status_title = tk.Label(status_frame, text="📊 System Status",
                               font=('Segoe UI', 12, 'bold'),
                               fg=self.colors['text_white'],
                               bg=self.colors['bg_light'])
        status_title.pack(pady=(10, 5), anchor=tk.W, padx=10)

        # Status indicators
        self.status_indicators = {}
        status_items = [
            ("Email Server", "offline"),
            ("Embedded Browser", "ready"),
            ("Discord Tools", "ready"),
            ("External Browser", "available")
        ]

        for item, status in status_items:
            indicator_frame = tk.Frame(status_frame, bg=self.colors['bg_light'])
            indicator_frame.pack(fill=tk.X, padx=10, pady=2)

            label = tk.Label(indicator_frame, text=f"{item}:",
                            font=('Segoe UI', 9),
                            fg=self.colors['text_gray'],
                            bg=self.colors['bg_light'])
            label.pack(side=tk.LEFT)

            status_label = tk.Label(indicator_frame, text=status.upper(),
                                   font=('Segoe UI', 9, 'bold'),
                                   fg=self.get_status_color(status),
                                   bg=self.colors['bg_light'])
            status_label.pack(side=tk.RIGHT)
            self.status_indicators[item] = status_label

    def create_right_panel(self, parent):
        """Create right panel for embedded Discord browser"""
        right_frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create embedded browser
        self.embedded_browser = EmbeddedDiscordBrowser(right_frame, self.colors)
        self.embedded_browser.browser_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Update URL entry reference for compatibility
        self.url_entry = self.embedded_browser.url_entry

        # Update status indicators
        if self.status_indicators.get("Embedded Browser"):
            self.status_indicators["Embedded Browser"].config(text="ACTIVE", fg=self.get_status_color("online"))
        if self.status_indicators.get("Discord Tools"):
            self.status_indicators["Discord Tools"].config(text="READY", fg=self.get_status_color("ready"))

    def create_status_bar(self, parent):
        """Create bottom status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_dark'], height=30)
        status_frame.pack(fill=tk.X, pady=(20, 0))
        status_frame.pack_propagate(False)

        # Status messages
        self.status_label = tk.Label(status_frame,
                                    text="Ready - RealLife AI Tools v1.0",
                                    font=('Segoe UI', 9),
                                    fg=self.colors['text_gray'],
                                    bg=self.colors['bg_dark'])
        self.status_label.pack(side=tk.LEFT, padx=20)

        # Version info
        version_label = tk.Label(status_frame,
                                text="v1.0.0",
                                font=('Segoe UI', 9),
                                fg=self.colors['text_gray'],
                                bg=self.colors['bg_dark'])
        version_label.pack(side=tk.RIGHT, padx=20)

    # Utility methods
    def get_status_color(self, status):
        """Get color for status indicator"""
        colors = {
            'online': '#4CAF50',
            'ready': '#2196F3',
            'connected': '#4CAF50',
            'offline': '#f44336',
            'error': '#f44336'
        }
        return colors.get(status.lower(), self.colors['text_gray'])

    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)

    # Button command methods
    def minimize_window(self):
        """Minimize the window"""
        self.root.iconify()

    def launch_brave_browser(self):
        """Launch Brave browser externally"""
        try:
            brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            if os.path.exists(brave_path):
                self.brave_process = subprocess.Popen([brave_path])
                self.update_status("Brave Browser launched externally")
                if self.status_indicators.get("External Browser"):
                    self.status_indicators["External Browser"].config(text="RUNNING", fg=self.get_status_color("online"))
                messagebox.showinfo("External Browser", "Brave browser opened in new window.\nUse the embedded browser for Discord operations.")
            else:
                messagebox.showerror("Error", "Brave browser not found at expected location")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Brave: {str(e)}")

    def open_email_server(self):
        """Open email server interface"""
        try:
            # Check if email server is running
            import requests
            response = requests.get("http://localhost:5000", timeout=2)
            if response.status_code == 200:
                # Open in embedded browser
                if self.embedded_browser:
                    self.embedded_browser.load_discord_page("http://localhost:5000")
                    self.update_status("Email server loaded in embedded browser")
                else:
                    webbrowser.open("http://localhost:5000")
                    self.update_status("Email server opened externally")
            else:
                raise Exception("Server not responding")
        except Exception as e:
            messagebox.showerror("Email Server", f"Email server not running.\nPlease start the email server first.\n\nError: {str(e)}")

    def create_email_account(self):
        """Create new email account"""
        if self.embedded_browser:
            self.embedded_browser.load_discord_page("http://localhost:5000/register")
            self.update_status("Email registration page loaded")
        else:
            try:
                webbrowser.open("http://localhost:5000/register")
                self.update_status("Email registration opened externally")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open email registration: {str(e)}")

    def view_email_inbox(self):
        """View email inbox"""
        if self.embedded_browser:
            self.embedded_browser.load_discord_page("http://localhost:5000/dashboard")
            self.update_status("Email dashboard loaded")
        else:
            try:
                webbrowser.open("http://localhost:5000/dashboard")
                self.update_status("Email dashboard opened externally")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open email dashboard: {str(e)}")

    def open_discord_website(self):
        """Open Discord website in embedded browser"""
        if self.embedded_browser:
            self.embedded_browser.load_discord_page("https://discord.com")
            self.update_status("Discord website loaded in embedded browser")
        else:
            try:
                webbrowser.open("https://discord.com")
                self.update_status("Discord website opened externally")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Discord: {str(e)}")

    def open_account_creator(self):
        """Open Discord account creator in embedded browser"""
        if self.embedded_browser:
            self.embedded_browser.load_discord_page("https://discord.com/register")
            self.update_status("Discord account creator loaded")
        else:
            messagebox.showinfo("Account Creator", "Use the embedded browser for account creation.\nClick 'Launch Brave Browser' to use external browser.")

    def open_bulk_operations(self):
        """Open bulk operations interface"""
        bulk_window = tk.Toplevel(self.root)
        bulk_window.title("Discord Bulk Operations")
        bulk_window.geometry("600x400")
        bulk_window.configure(bg=self.colors['bg_dark'])

        title_label = tk.Label(bulk_window, text="Discord Bulk Account Operations",
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['chrome_blue'],
                              bg=self.colors['bg_dark'])
        title_label.pack(pady=20)

        # Bulk operations content
        content_frame = tk.Frame(bulk_window, bg=self.colors['bg_medium'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        operations = [
            ("Create Multiple Accounts", "Create multiple Discord accounts automatically"),
            ("Email Verification", "Verify email addresses for accounts"),
            ("Server Joining", "Join Discord servers with created accounts"),
            ("Profile Setup", "Configure account profiles and avatars"),
            ("Token Management", "Manage account tokens and sessions")
        ]

        for op_name, op_desc in operations:
            op_frame = tk.Frame(content_frame, bg=self.colors['bg_light'], pady=10, padx=15)
            op_frame.pack(fill=tk.X, pady=5)

            name_label = tk.Label(op_frame, text=op_name,
                                 font=('Segoe UI', 12, 'bold'),
                                 fg=self.colors['text_white'],
                                 bg=self.colors['bg_light'])
            name_label.pack(anchor=tk.W)

            desc_label = tk.Label(op_frame, text=op_desc,
                                 font=('Segoe UI', 10),
                                 fg=self.colors['text_gray'],
                                 bg=self.colors['bg_light'])
            desc_label.pack(anchor=tk.W)

            btn = tk.Button(op_frame, text="Execute",
                           font=('Segoe UI', 10),
                           bg=self.colors['chrome_blue'],
                           fg=self.colors['text_white'],
                           borderwidth=0,
                           padx=15, pady=5,
                           command=lambda n=op_name: self.execute_bulk_operation(n))
            btn.pack(anchor=tk.E)

        close_btn = tk.Button(bulk_window, text="Close",
                             font=('Segoe UI', 10),
                             bg=self.colors['bg_dark'],
                             fg=self.colors['text_white'],
                             borderwidth=0,
                             padx=20, pady=8,
                             command=bulk_window.destroy)
        close_btn.pack(pady=(0, 20))

        self.update_status("Bulk operations interface opened")

    def browser_back(self):
        """Browser back button"""
        if self.embedded_browser:
            self.embedded_browser.go_back()
            self.update_status("Browser back navigation")

    def browser_forward(self):
        """Browser forward button"""
        if self.embedded_browser:
            self.embedded_browser.go_forward()
            self.update_status("Browser forward navigation")

    def browser_refresh(self):
        """Browser refresh button"""
        if self.embedded_browser:
            self.embedded_browser.refresh()
            self.update_status("Browser refresh")

    def browser_home(self):
        """Browser home button"""
        if self.embedded_browser:
            self.embedded_browser.go_home()
            self.update_status("Navigated to Discord home")

    def navigate_to_url(self):
        """Navigate to entered URL"""
        if self.embedded_browser:
            self.embedded_browser.navigate_to_url()
        else:
            url = self.url_entry.get()
            if url:
                try:
                    webbrowser.open(url)
                    self.update_status(f"Opened: {url}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to navigate: {str(e)}")

    def execute_bulk_operation(self, operation_name):
        """Execute bulk operation"""
        operations = {
            "Create Multiple Accounts": "Account creation would automate Discord registration here.",
            "Email Verification": "Email verification would check account emails here.",
            "Server Joining": "Server joining would add accounts to Discord servers here.",
            "Profile Setup": "Profile setup would configure account details here.",
            "Token Management": "Token management would handle account sessions here."
        }

        message = operations.get(operation_name, f"Operation '{operation_name}' is not yet implemented.")
        messagebox.showinfo("Bulk Operation", f"{operation_name}\n\n{message}")

        self.update_status(f"Bulk operation attempted: {operation_name}")

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernChromeGUI()
    app.run()
