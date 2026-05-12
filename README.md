# Armstrong Number App

A full-stack web application for checking and finding Armstrong (Narcissistic) numbers, built with Flask and SQLite/PostgreSQL. This is an eProject for Aptech Semester 4 & 5.

## What is an Armstrong Number?

An Armstrong number (also called a Narcissistic number) is a number that equals the sum of its digits, each raised to the power of the total number of digits.

**Example:** 153 is an Armstrong number because:
```
153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153
```

## Features

- **User Authentication** — Registration and login with secure password hashing (Werkzeug)
- **Email OTP Verification** — Optional 6-digit OTP sent via Gmail SMTP (works without email config too — see Setup)
- **Forgot Password** — Token-based password reset via email
- **Single Number Check** — Enter any number to check if it's an Armstrong number
- **Range Search** — Find all Armstrong numbers within a range (up to 1,000,000)
- **Attempts History** — View past checks with pagination and CSV export
- **User Settings** — Update profile, change password, delete account
- **Feedback System** — 1–5 star rating with message
- **Admin Dashboard** — View all users, attempts, and feedback (admin only)
- **Contact Page** — Static contact information

## Tech Stack

- **Backend:** Python 3, Flask
- **Database:** SQLite (default) / PostgreSQL (via Supabase)
- **ORM:** Flask-SQLAlchemy
- **Auth:** Flask-Login
- **Email:** Flask-Mail (optional)
- **Templates:** Jinja2
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Favour-Ikec/armstrong-number-app.git
   cd armstrong-number-app
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv

   # macOS / Linux
   source venv/bin/activate

   # Windows (PowerShell)
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Open in your browser:**
   ```
   http://127.0.0.1:5000
   ```

The app uses SQLite by default, so no database setup is needed. You can register an account and start using the app immediately.

### Email Configuration (Optional)

Email OTP verification is **optional**. Without it, users are auto-verified on registration and can log in directly. To enable email verification, create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USE_TLS=False
MAIL_USERNAME=your-gmail@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-gmail@gmail.com
```

**Note:** For `MAIL_PASSWORD`, you need a [Google App Password](https://myaccount.google.com/apppasswords), not your regular Gmail password. This requires 2-Step Verification to be enabled on your Google account.

### Using PostgreSQL (Optional)

To use PostgreSQL instead of SQLite, add this to your `.env` file:

```env
DATABASE_URL=postgresql://user:password@host:port/database
```

## Project Structure

```
armstrong-number-app/
├── app/
│   ├── __init__.py          # App factory, config, extensions
│   ├── models.py            # User, Attempt, Feedback models
│   ├── routes.py            # All route handlers
│   ├── email_utils.py       # OTP generation, email sending, token helpers
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom styles
│   │   ├── js/
│   │   │   └── app.js       # Client-side JavaScript
│   │   └── images/          # SVG illustrations
│   └── templates/
│       ├── base.html         # Base layout template
│       ├── home.html         # Landing page
│       ├── login.html        # Login form
│       ├── register.html     # Registration form
│       ├── verify_otp.html   # OTP verification page
│       ├── check.html        # Single number checker
│       ├── range.html        # Range search
│       ├── attempts.html     # Attempts history
│       ├── settings.html     # User settings
│       ├── feedback.html     # Feedback form
│       ├── contact.html      # Contact page
│       ├── admin.html        # Admin dashboard
│       ├── forgot_password.html
│       ├── reset_password.html
│       └── emails/           # Email templates
│           ├── verify_otp.html
│           └── reset_password.html
├── run.py                    # Entry point
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## Team

| Name | Student ID | Role |
|------|-----------|------|
| Favour Ikechukwu Agugbue | 1649583 | Lead Developer — Backend, authentication, email system, admin dashboard |
| Samuel Tofunmi Oyegbola | 1607440 | Frontend — Templates, UI/UX, styling |
| Miracle Chidiebere Richard | 1626476 | Features — Armstrong logic, range search, attempts history |
| Mohammed Abdulmalik | 1528140 | Testing & Documentation — QA, project report |

## Submission

- **Project:** Python/R — Armstrong Number
- **Start Date:** 6 April 2026
- **Deadline:** 27 April 2026

## License

This project was built as an academic eProject for Aptech Computer Education.
