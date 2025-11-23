#!/usr/bin/env python3
"""
Local Email Server for Discord Account Management
Features: User registration, login, email sending/receiving, web interface
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import os
import secrets
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time

app = Flask(__name__)

# Vercel-compatible configuration
if os.environ.get('VERCEL'):
    # Use Vercel's temporary directory for database
    db_path = '/tmp/email_server.db'
else:
    db_path = 'email_server.db'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration (for local testing - in production, use proper SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change for your email provider
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', 'your-password')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(120), unique=True)

class EmailMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', backref=db.backref('sent_emails', lazy=True))

class ReceivedEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('received_emails', lazy=True))

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        verification_token = secrets.token_urlsafe(32)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            verification_token=verification_token
        )

        db.session.add(new_user)
        db.session.commit()

        # Send verification email
        send_verification_email(email, verification_token)

        flash('Registration successful! Please check your email to verify your account.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            if not user.is_verified:
                flash('Please verify your email before logging in.', 'warning')
                return redirect(url_for('login'))

            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/verify/<token>')
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()

    if user:
        user.is_verified = True
        user.verification_token = None
        db.session.commit()
        flash('Email verified successfully! You can now log in.', 'success')
    else:
        flash('Invalid verification token.', 'error')

    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    emails = ReceivedEmail.query.filter_by(user_id=user.id).order_by(ReceivedEmail.received_at.desc()).limit(10).all()

    return render_template('dashboard.html', user=user, emails=emails)

@app.route('/compose', methods=['GET', 'POST'])
def compose_email():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        body = request.form['body']

        user = User.query.get(session['user_id'])

        # Save sent email
        sent_email = EmailMessage(
            sender_id=user.id,
            recipient_email=recipient,
            subject=subject,
            body=body
        )
        db.session.add(sent_email)
        db.session.commit()

        # Send email (in production, use proper SMTP)
        try:
            send_email(recipient, subject, body, user.email)
            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Email saved but sending failed: {str(e)}', 'warning')

        return redirect(url_for('dashboard'))

    return render_template('compose.html')

@app.route('/inbox')
def inbox():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    emails = ReceivedEmail.query.filter_by(user_id=user.id).order_by(ReceivedEmail.received_at.desc()).all()

    return render_template('inbox.html', user=user, emails=emails)

@app.route('/email/<int:email_id>')
def view_email(email_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    email = ReceivedEmail.query.filter_by(id=email_id, user_id=user.id).first()

    if email:
        email.is_read = True
        db.session.commit()
        return render_template('view_email.html', user=user, email=email)

    flash('Email not found', 'error')
    return redirect(url_for('inbox'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/api/emails/unread')
def get_unread_count():
    if 'user_id' not in session:
        return jsonify({'count': 0})

    count = ReceivedEmail.query.filter_by(user_id=session['user_id'], is_read=False).count()
    return jsonify({'count': count})

# Utility functions
def send_verification_email(email, token):
    """Send email verification link"""
    try:
        msg = Message('Verify Your Email',
                     sender=app.config['MAIL_DEFAULT_SENDER'],
                     recipients=[email])

        verification_url = url_for('verify_email', token=token, _external=True)
        msg.body = f'Please click the following link to verify your email: {verification_url}'

        # For local testing, we'll simulate sending
        print(f"Verification email would be sent to {email} with token: {token}")
        print(f"Verification URL: {verification_url}")

        # In production: mail.send(msg)
    except Exception as e:
        print(f"Failed to send verification email: {e}")

def send_email(recipient, subject, body, sender_email):
    """Send email using SMTP"""
    try:
        # For local testing, we'll simulate sending
        print(f"Email would be sent from {sender_email} to {recipient}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")

        # In production, use proper SMTP:
        # msg = MIMEMultipart()
        # msg['From'] = sender_email
        # msg['To'] = recipient
        # msg['Subject'] = subject
        # msg.attach(MIMEText(body, 'plain'))
        #
        # server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        # server.starttls()
        # server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        # server.sendmail(sender_email, recipient, msg.as_string())
        # server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

def create_sample_emails():
    """Create sample emails for testing"""
    with app.app_context():
        # Create a test user if none exists
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
            test_user = User(
                username='testuser',
                email='test@example.com',
                password=hashed_password,
                is_verified=True
            )
            db.session.add(test_user)
            db.session.commit()

        # Add sample received emails
        sample_emails = [
            {
                'sender_email': 'welcome@discord.com',
                'subject': 'Welcome to Discord!',
                'body': 'Thank you for joining Discord. Get started by creating your first server!'
            },
            {
                'sender_email': 'noreply@discord.com',
                'subject': 'Verify Your Discord Account',
                'body': 'Please verify your email to complete your Discord account setup.'
            }
        ]

        for email_data in sample_emails:
            existing = ReceivedEmail.query.filter_by(
                user_id=test_user.id,
                sender_email=email_data['sender_email'],
                subject=email_data['subject']
            ).first()

            if not existing:
                received_email = ReceivedEmail(
                    user_id=test_user.id,
                    sender_email=email_data['sender_email'],
                    subject=email_data['subject'],
                    body=email_data['body']
                )
                db.session.add(received_email)

        db.session.commit()

# Template filters
@app.template_filter('datetime')
def format_datetime(value):
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return value.strftime('%Y-%m-%d %H:%M')

# Initialize database and create sample data when the module is imported
try:
    with app.app_context():
        db.create_all()
        create_sample_emails()
        print("Database initialized successfully")
except Exception as e:
    print(f"Database initialization error: {e}")
    # Continue anyway - the app should still work

if __name__ == '__main__':
    print("Email Server starting on http://localhost:5000")
    print("Test account: test@example.com / password")
    app.run(debug=True, host='0.0.0.0', port=5000)
