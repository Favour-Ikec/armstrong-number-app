"""
Email utilities: token generation/verification + email sending helpers.
Used for email verification on signup and forgot-password flow.
"""
from flask import current_app, render_template, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app import mail


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


def send_verification_email(user):
    token = generate_token(user.email, salt='email-verify')
    verify_url = url_for('main.verify_email', token=token, _external=True)
    html = render_template(
        'emails/verify_email.html',
        user=user,
        verify_url=verify_url
    )
    text = (
        f"Hi {user.name},\n\n"
        f"Please verify your email for the Armstrong Number App by visiting:\n"
        f"{verify_url}\n\n"
        f"This link expires in 1 hour.\n\n"
        f"If you didn't create an account, you can ignore this email."
    )
    return send_email(
        user.email,
        'Verify your email — Armstrong Number App',
        html,
        text
    )


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
