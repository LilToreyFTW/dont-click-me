// Chrome-style Email System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeInterface();
    setupEventListeners();
});

function initializeInterface() {
    // Add fade-in animation to content
    const contentArea = document.querySelector('.content-body');
    if (contentArea) {
        contentArea.classList.add('fade-in');
    }

    // Update status bar with current time
    updateStatusBar();

    // Check for unread emails periodically
    if (document.querySelector('.email-list')) {
        setInterval(checkUnreadEmails, 30000); // Check every 30 seconds
    }

    // Initialize window controls
    initializeWindowControls();
}

function setupEventListeners() {
    // Navigation highlighting
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', validateForm);
    });

    // Password confirmation
    const passwordFields = document.querySelectorAll('input[type="password"]');
    if (passwordFields.length >= 2) {
        const confirmPassword = passwordFields[1];
        confirmPassword.addEventListener('input', function() {
            const password = passwordFields[0].value;
            const confirm = this.value;

            if (password !== confirm) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

function initializeWindowControls() {
    const minimizeBtn = document.querySelector('.control-btn.minimize');
    const closeBtn = document.querySelector('.control-btn.close');

    if (minimizeBtn) {
        minimizeBtn.addEventListener('click', function() {
            // In a real application, this would minimize the window
            alert('Minimize functionality would be implemented in desktop app');
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to close the application?')) {
                window.close();
            }
        });
    }
}

function validateForm(e) {
    const form = e.target;
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#ea4335';
            isValid = false;
        } else {
            input.style.borderColor = '#404040';
        }
    });

    if (!isValid) {
        e.preventDefault();
        showAlert('Please fill in all required fields', 'error');
        return false;
    }

    return true;
}

function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} fade-in`;

    const iconMap = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    };

    alertDiv.innerHTML = `
        <i class="${iconMap[type]}"></i>
        <span>${message}</span>
    `;

    const contentBody = document.querySelector('.content-body');
    if (contentBody) {
        contentBody.insertBefore(alertDiv, contentBody.firstChild);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
    }
}

function updateStatusBar() {
    const statusText = document.querySelector('.status-text');
    if (statusText) {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        statusText.textContent = `Ready - ${timeString}`;
    }
}

async function checkUnreadEmails() {
    try {
        const response = await fetch('/api/emails/unread');
        const data = await response.json();

        updateUnreadCount(data.count);
    } catch (error) {
        console.error('Failed to check unread emails:', error);
    }
}

function updateUnreadCount(count) {
    const inboxNav = document.querySelector('.nav-item[href="/inbox"]');
    if (inboxNav) {
        // Remove existing badge
        const existingBadge = inboxNav.querySelector('.unread-badge');
        if (existingBadge) {
            existingBadge.remove();
        }

        if (count > 0) {
            const badge = document.createElement('span');
            badge.className = 'unread-badge';
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.cssText = `
                background: #ea4335;
                color: white;
                border-radius: 10px;
                padding: 2px 6px;
                font-size: 11px;
                font-weight: 600;
                margin-left: auto;
                margin-right: 10px;
            `;
            inboxNav.appendChild(badge);
        }
    }
}

// Email composition helper
function initializeEmailComposer() {
    const composerForm = document.getElementById('compose-form');
    if (composerForm) {
        const textarea = composerForm.querySelector('textarea');
        if (textarea) {
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        }
    }
}

// Dashboard statistics
function updateDashboardStats() {
    // This would typically fetch real stats from the server
    const stats = {
        totalEmails: 42,
        unreadEmails: 7,
        sentToday: 3
    };

    Object.keys(stats).forEach(key => {
        const element = document.getElementById(`${key}-stat`);
        if (element) {
            element.textContent = stats[key];
        }
    });
}

// Smooth scrolling for anchor links
document.addEventListener('click', function(e) {
    const link = e.target.closest('a[href^="#"]');
    if (link) {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit forms
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeForm = document.activeElement.closest('form');
        if (activeForm) {
            activeForm.dispatchEvent(new Event('submit'));
        }
    }

    // Escape to close modals (if any)
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

// Auto-refresh functionality for email lists
let autoRefreshInterval;

function startAutoRefresh() {
    if (document.querySelector('.email-list')) {
        autoRefreshInterval = setInterval(() => {
            location.reload();
        }, 60000); // Refresh every minute
    }
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
}

// Initialize specific page features
document.addEventListener('DOMContentLoaded', function() {
    initializeInterface();
    setupEventListeners();

    // Page-specific initializations
    if (document.getElementById('compose-form')) {
        initializeEmailComposer();
    }

    if (document.querySelector('.dashboard-stats')) {
        updateDashboardStats();
    }

    // Start auto-refresh for email pages
    startAutoRefresh();

    // Clean up on page unload
    window.addEventListener('beforeunload', stopAutoRefresh);
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showAlert('Copied to clipboard!', 'success');
    }, function(err) {
        console.error('Could not copy text: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showAlert('Copied to clipboard!', 'success');
        } catch (err) {
            showAlert('Failed to copy to clipboard', 'error');
        }
        document.body.removeChild(textArea);
    });
}

// Export functions for global use
window.EmailSystem = {
    showAlert,
    copyToClipboard,
    updateUnreadCount
};
