# Armstrong Number Web App

A Python Flask web application for checking and finding Armstrong numbers. Built as an eProject for Aptech (Semester 5).

## What is an Armstrong Number?

An Armstrong number is a number equal to the sum of its own digits raised to the power of the number of digits. For example, 153 = 1³ + 5³ + 3³ = 153.

## Features

- User registration and login with secure password hashing
- Check if a single number is an Armstrong number
- Find all Armstrong numbers within a given range
- View history of all past attempts
- User profile settings (update/delete account, add address)
- Contact Us page
- Feedback submission form

## Team

| Name | Student ID | Role |
|------|-----------|------|
| Favour Ikechukwu Agugbue | Student1649583 | Flask setup, Armstrong logic, demo video |
| Samuel Tofunmi Oyegbola | Student1607440 | Auth (registration, login, settings) |
| Miracle Chidiebere Richard | Student1626476 | Attempts history, home page, styling |
| Mohammed Abdulmalik | Student1528140 | Contact, feedback, report coordination |

## Tech Stack

- Python 3
- Flask
- Flask-SQLAlchemy (SQLite)
- Flask-Login
- Bootstrap 5

## Getting Started

1. Clone the repo:

git clone https://github.com/Favour-Ikec/armstrong-number-app.git
cd armstrong-number-app

2. Create a virtual environment:
   - Mac: `python3 -m venv venv && source venv/bin/activate`
   - Windows: `python -m venv venv && venv\Scripts\activate`

3. Install dependencies:
pip install -r requirements.txt

4. Run the app:
python run.py

5. Open http://127.0.0.1:5000 in your browser.

## Workflow Rules

- Never push directly to `main`
- Always create a branch: `git checkout -b feature/your-task-name`
- Push your branch and open a Pull Request
- Tag a teammate to review before merging
- Check the Issues tab for your assigned tasks

## Project Structure
armstrong-number-app/
├── app/
│   ├── init.py          # App factory + config
│   ├── models.py            # User, Attempt, Feedback models
│   ├── routes.py            # All routes
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── settings.html
│   │   ├── check.html
│   │   ├── range.html
│   │   ├── attempts.html
│   │   ├── contact.html
│   │   └── feedback.html
│   └── static/
│       └── css/
│           └── style.css
├── docs/                    # eProject report, DFDs, screenshots
├── run.py                   # Entry point
├── requirements.txt
└── README.md



## Deadline

Submission due: 27 April 2026
