# Armstrong Number Web App

A full-stack web application for checking and finding Armstrong (Narcissistic) numbers, built with Flask and PostgreSQL.

**eProject — Aptech Semester 4**

---

## What is an Armstrong Number?

An Armstrong number (also known as a Narcissistic number) is a number that equals the sum of its own digits, each raised to the power of the number of digits.

**Example:** 153 is an Armstrong number because it has 3 digits, and:
1³ + 5³ + 3³ = 1 + 125 + 27 = 153
---

## Features

- **User Registration & Login** — Secure authentication with password hashing (Werkzeug)
- **OTP Email Verification** — 6-digit code sent via email on signup (expires in 10 minutes)
- **Forgot Password** — Password reset via secure email link (expires in 1 hour)
- **Single Number Check** — Enter any number to check if it's an Armstrong number
- **Range Search** — Find all Armstrong numbers within a given range (up to 1,000,000)
- **Attempts History** — View and export (CSV) all past checks
- **User Settings** — Update profile, change password (prevents reuse of old password), delete account
- **Feedback System** — Submit feedback with a 1–5 star rating
- **Admin Dashboard** — View all users, total attempts, feedback, and average rating
- **Contact Us** — Static contact information page

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python 3, Flask, Flask-SQLAlchemy   |
| Database   | PostgreSQL (Supabase) / SQLite      |
| Auth       | Flask-Login, Werkzeug               |
| Email      | Flask-Mail (Gmail SMTP)             |
| Frontend   | Jinja2, Bootstrap 5, Font Awesome   |
| Deployment | GitHub                              |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Favour-Ikec/armstrong-number-app.git
cd armstrong-number-app
```

### 2. Create a virtual environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file called `.env` in the root of the project with the following variables:
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

> **Note:** If you don't have a PostgreSQL database, you can leave out the `DATABASE_URL` line and the app will automatically use a local SQLite database.

> **Gmail App Password:** To send emails, you need a Gmail App Password. Go to your Google Account → Security → 2-Step Verification → App Passwords, and generate one.

### 5. Run the application

```bash
python run.py
```

### 6. Open in your browser
http://127.0.0.1:5000
---

## Project Structure
armstrong-number-app/
├── app/
│   ├── init.py          # App factory, config, extensions
│   ├── models.py            # User, Attempt, Feedback models
│   ├── routes.py            # All routes and business logic
│   ├── email_utils.py       # OTP generation, email sending, token helpers
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── home.html
│       ├── register.html
│       ├── login.html
│       ├── verify_otp.html
│       ├── check.html
│       ├── range.html
│       ├── attempts.html
│       ├── settings.html
│       ├── feedback.html
│       ├── contact.html
│       ├── admin.html
│       ├── forgot_password.html
│       ├── reset_password.html
│       └── emails/
│           ├── verify_otp.html
│           └── reset_password.html
├── .env                     # Environment variables (not in repo)
├── .gitignore
├── requirements.txt
├── run.py                   # Entry point
└── README.md

---

## Team

| Name | Student ID | Responsibilities |
|------|-----------|-----------------|
| Favour Ikechukwu Agugbue | Student1649583 | Flask setup, Armstrong logic, OTP verification, demo video |
| Samuel Tofunmi Oyegbola | Student1649578 | Authentication, registration, login, settings |
| Miracle Chidiebere Richard | Student1649574 | Attempts history, home page, UI/UX styling |
| Mohammed Abdulmalik | Student1649569 | Contact page, feedback system, report coordination |

---

## Submission Deadline

**27 April 2026**