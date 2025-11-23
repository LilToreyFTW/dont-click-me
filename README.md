# RealLife AI Tools - Discord Account Manager

A comprehensive GUI application with integrated email server for Discord account management.

## Features

### 🎨 Modern GUI Interface
- **1920x1080 resolution** with chrome-style design
- **Deep chrome blues, blacks, and whites** color scheme
- **Professional 3D styling** with modern UI elements
- **Embedded Discord Browser** - Browse Discord directly in the GUI
- **External Brave Browser** launcher for full web access
- **Real-time status indicators** and system monitoring

### 🌐 Embedded Discord Browser
- **Discord-optimized interface** within the GUI
- **Navigation controls** (back, forward, refresh, home)
- **Interactive elements** - clickable links and buttons
- **Login simulation** and account creation flows
- **No external windows** - everything stays within the GUI
- **History management** and URL navigation

### 📧 Email Server System
- **User registration and authentication**
- **Email composition and sending**
- **Inbox management** with read/unread status
- **Secure password hashing** with Flask-Bcrypt
- **SQLite database** for data persistence
- **Web-based interface** with responsive design

### 🔧 Technical Features
- **Flask web framework** for email server
- **Tkinter GUI** for desktop interface
- **RESTful API** endpoints
- **Real-time updates** and notifications
- **Cross-platform compatibility**

## Installation

### Prerequisites
- Python 3.8 or higher
- Brave Browser installed at default location
- Windows 10/11 (or compatible OS)

### Setup Steps

1. **Clone or download** this project
2. **Navigate to the project directory**:
   ```bash
   cd DiscordAccount-making
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the system**:
   ```bash
   python run_system.py
   ```

## Usage

### First Time Setup
1. Launch the application using `python run_system.py`
2. The email server will start automatically on `http://localhost:5000`
3. The GUI will open showing the main interface

### Creating an Account
1. Open the email server in your browser: `http://localhost:5000`
2. Click "Register" to create a new account
3. Fill in your details and verify your email
4. Or use the test account: `test@example.com` / `password`

### Using the GUI
- **Brave Browser**: Click to launch Brave Browser
- **Email Server**: Opens the web interface
- **Discord Tools**: Access Discord-related features
- **Status Indicators**: Monitor system health

### Email Features
- **Compose**: Write and send emails
- **Inbox**: View received emails
- **Dashboard**: Overview of your email activity
- **Settings**: Manage your account preferences

## Project Structure

```
DiscordAccount-making/
├── gui_main.py              # Main GUI application
├── email_server.py         # Flask email server
├── run_system.py           # System launcher
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/              # Flask HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
├── static/                 # CSS and JavaScript files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── email_server.db        # SQLite database (created automatically)
```

## Configuration

### Email Server Settings
Edit `email_server.py` to configure:
- Email SMTP settings
- Database connection
- Security settings

### GUI Customization
Modify `gui_main.py` to change:
- Window size and styling
- Browser paths
- Interface elements

## Security Notes

- **Local Development Only**: This system is designed for local development
- **No Production Email**: Uses simulation for email sending
- **Basic Authentication**: Suitable for personal use only
- **SQLite Database**: Not suitable for high-traffic production

## Browser Integration

The GUI integrates with Brave Browser installed at:
```
C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe
```

Modify the path in `gui_main.py` if installed elsewhere.

## API Endpoints

### Email Server API
- `GET /` - Home page
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /dashboard` - User dashboard
- `POST /compose` - Send email
- `GET /inbox` - View inbox
- `GET /api/emails/unread` - Unread count

## Troubleshooting

### Common Issues

1. **"Brave browser not found"**
   - Verify Brave installation path
   - Update path in `gui_main.py`

2. **"Port 5000 already in use"**
   - Close other applications using port 5000
   - Or modify port in `email_server.py`

3. **"Import errors"**
   - Ensure all requirements are installed
   - Check Python version compatibility

4. **"Database errors"**
   - Delete `email_server.db` and restart
   - Check file permissions

### Logs and Debugging
- GUI errors appear in console/terminal
- Email server logs to console
- Enable debug mode in Flask for detailed logs

## Deployment

### Vercel Deployment
1. Go to [Vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your Git repository: `https://github.com/LilToreyFTW/dont-click-me.git`
4. Vercel will automatically detect the `vercel.json` configuration
5. Click "Deploy"
6. Your email system will be live at the provided Vercel URL

### Local Development
Run the system locally:
```bash
python run_system.py
```

### GUI Desktop Application
The desktop GUI (Tkinter) runs locally with a fully embedded Discord browser. All Discord operations happen within the GUI interface without opening external windows.

#### Embedded Browser Features
- **Discord Home Page**: Welcome screen with login/register options
- **Login Interface**: Simulated Discord login with form fields
- **Registration Flow**: Account creation with validation
- **App Interface**: Mock Discord app with servers and channels
- **Interactive Elements**: Clickable buttons and links
- **Navigation History**: Back/forward through browsing history

#### External Browser Option
- **Brave Browser Integration**: Launch external browser for full web access
- **Dual Browsing Modes**: Choose between embedded or external browsing

## Development

### Adding New Features
1. GUI features: Modify `gui_main.py`
2. Email features: Update `email_server.py` and templates
3. Styling: Edit `static/css/style.css`
4. JavaScript: Modify `static/js/main.js`

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Test changes thoroughly

## License

This project is for educational and personal use only.

## Disclaimer

This system is a demonstration of GUI and web development concepts. It is not intended for production use without proper security auditing and infrastructure setup.

---

**RealLife AI Tools v1.0**
Built with Flask, Tkinter, and modern web technologies.
