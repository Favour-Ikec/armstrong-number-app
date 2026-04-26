"""
Email utilities: token generation/verification + email sending helpers.
Used for email verification on signup and forgot-password flow.
"""
import random
from datetime import datetime, timedelta
from flask import current_app, render_template, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app import mail, db


# ──────────────────────────────────────
# Token helpers (signed + time-limited)
# ──────────────────────────────────────
def _serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def generate_token(email, salt):
    """Generate a signed, time-limited token tied to an email + purpose (salt)."""
    return _serializer().dumps(email, salt=salt)


def verify_token(token, salt, max_age=3600):
    """
    Verify a token. Returns the email if valid, None if invalid/expired.
    max_age is in seconds (default 1 hour).
    """
    try:
        email = _serializer().loads(token, salt=salt, max_age=max_age)
        return email
    except (BadSignature, SignatureExpired):
        return None


# ──────────────────────────────────────
# Email sending
# ──────────────────────────────────────
def send_email(to, subject, html_body, text_body=None):
    """Send an email. Silently logs errors if mail isn't configured."""
    try:
        msg = Message(subject, recipients=[to])
        msg.body = text_body or ''
        msg.html = html_body
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f'Failed to send email to {to}: {e}')
        return False


def generate_otp():
    """Generate a random 6-digit OTP code."""
    return str(random.randint(100000, 999999))


def send_otp_email(user):
    """Generate an OTP, save it to the user, and send it via email."""
    otp = generate_otp()
    user.otp_code = otp
    user.otp_expires = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    html = render_template(
        'emails/verify_otp.html',
        user=user,
        otp_code=otp
    )
    text = (
        f"Hi {user.name},\n\n"
        f"Your verification code for the Armstrong Number App is:\n\n"
        f"{otp}\n\n"
        f"This code expires in 10 minutes.\n\n"
        f"If you didn't create an account, you can ignore this email."
    )
    return send_email(
        user.email,
        'Your Verification Code — Armstrong Number App',
        html,
        text
    )


def verify_otp(user, code):
    """Check if the OTP code is correct and not expired. Returns True/False."""
    if not user.otp_code or not user.otp_expires:
        return False
    if user.otp_code != code:
        return False
    if datetime.utcnow() > user.otp_expires:
        return False
    # OTP is valid — clear it so it can't be reused
    user.otp_code = None
    user.otp_expires = None
    db.session.commit()
    return True


def send_password_reset_email(user):
    token = generate_token(user.email, salt='password-reset')
    reset_url = url_for('main.reset_password', token=token, _external=True)
    html = render_template(
        'emails/reset_password.html',
        user=user,
        reset_url=reset_url
    )
    text = (
        f"Hi {user.name},\n\n"
        f"You requested a password reset for the Armstrong Number App.\n"
        f"Reset your password here: {reset_url}\n\n"
        f"This link expires in 1 hour.\n\n"
        f"If you didn't request this, you can safely ignore this email."
    )
    return send_email(
        user.email,
        'Reset your password — Armstrong Number App',
        html,
        text
    )