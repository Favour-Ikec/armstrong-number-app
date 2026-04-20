from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Attempt, Feedback
import csv
import io
from flask import Response
from sqlalchemy import func
from app.email_utils import (
    generate_token,
    verify_token,
    send_verification_email,
    send_password_reset_email,
)

main = Blueprint('main', __name__)


# ──────────────────────────────────────
# Home
# ──────────────────────────────────────
@main.route('/')
def home():
    return render_template('home.html')


# ──────────────────────────────────────
# Auth: Register
# ──────────────────────────────────────
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        contact = request.form.get('contact_number', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # Basic server-side validation
        if not all([name, email, contact, username, password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('main.register'))

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('main.register'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return redirect(url_for('main.register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('main.register'))

        user = User(name=name, email=email, contact_number=contact, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Send verification email
        send_verification_email(user)

        flash('Account created! Please check your email to verify your account.', 'success')
        return redirect(url_for('main.verification_sent', email=email))

    return render_template('register.html')


# ──────────────────────────────────────
# Auth: Login / Logout
# ──────────────────────────────────────
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if not user.email_verified:
                flash(
                    'Please verify your email before logging in. '
                    'Check your inbox, or request a new verification link below.',
                    'error'
                )
                return redirect(url_for('main.verification_sent', email=user.email))

            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))

        flash('Invalid username or password.', 'error')
        return redirect(url_for('main.login'))

    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))


# ──────────────────────────────────────
# Settings
# ──────────────────────────────────────
@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update':
            current_user.name = request.form.get('name', current_user.name).strip()
            current_user.email = request.form.get('email', current_user.email).strip()
            current_user.contact_number = request.form.get('contact_number', current_user.contact_number).strip()
            current_user.address = request.form.get('address', '').strip()

            new_password = request.form.get('new_password', '')
            if new_password:
                if current_user.check_password(new_password):
                    flash('New password cannot be the same as your old password.', 'error')
                    return redirect(url_for('main.settings'))
                current_user.set_password(new_password)

            db.session.commit()
            flash('Profile updated.', 'success')

        elif action == 'delete':
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            flash('Account deleted.', 'success')
            return redirect(url_for('main.home'))

        return redirect(url_for('main.settings'))

    return render_template('settings.html')


# ──────────────────────────────────────
# Armstrong: Check single number
# ──────────────────────────────────────
def is_armstrong(n):
    digits = str(n)
    power = len(digits)
    return n == sum(int(d) ** power for d in digits)


@main.route('/check', methods=['GET', 'POST'])
@login_required
def check():
    result = None
    number = ''

    if request.method == 'POST':
        number = request.form.get('number', '').strip()

        if not number.isdigit() or int(number) < 0:
            flash('Please enter a valid positive integer.', 'error')
        else:
            n = int(number)
            if is_armstrong(n):
                result = f'{n} is an Armstrong Number'
            else:
                result = f'{n} is Not an Armstrong Number'

            # Save attempt
            attempt = Attempt(
                user_id=current_user.id,
                input_type='single',
                input_value=str(n),
                result=result
            )
            db.session.add(attempt)
            db.session.commit()

    return render_template('check.html', result=result, number=number)


# ──────────────────────────────────────
# Armstrong: Range mode
# ──────────────────────────────────────
@main.route('/range', methods=['GET', 'POST'])
@login_required
def range_check():
    results = None
    min_val = ''
    max_val = ''

    if request.method == 'POST':
        min_val = request.form.get('min', '').strip()
        max_val = request.form.get('max', '').strip()

        if not min_val.isdigit() or not max_val.isdigit():
            flash('Please enter valid positive integers.', 'error')
        elif int(min_val) >= int(max_val):
            flash('Minimum must be less than maximum.', 'error')
        elif int(max_val) > 1_000_000:
            flash('Maximum value cannot exceed 1,000,000.', 'error')
        else:
            lo, hi = int(min_val), int(max_val)
            armstrong_numbers = [n for n in range(lo, hi + 1) if is_armstrong(n)]
            results = {
                'numbers': armstrong_numbers,
                'count': len(armstrong_numbers)
            }

            # Save attempt
            result_text = f"Found {results['count']} Armstrong numbers in range {lo}-{hi}: {armstrong_numbers}"
            attempt = Attempt(
                user_id=current_user.id,
                input_type='range',
                input_value=f'{lo}-{hi}',
                result=result_text
            )
            db.session.add(attempt)
            db.session.commit()

    return render_template('range.html', results=results, min_val=min_val, max_val=max_val)


# ──────────────────────────────────────
# Attempts history
# ──────────────────────────────────────
@main.route('/attempts')
@login_required
def attempts():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    pagination = Attempt.query.filter_by(user_id=current_user.id) \
        .order_by(Attempt.timestamp.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'attempts.html',
        attempts=pagination.items,
        pagination=pagination
    )


# ──────────────────────────────────────
# Contact Us
# ──────────────────────────────────────
@main.route('/contact')
def contact():
    return render_template('contact.html')


# ──────────────────────────────────────
# Feedback
# ──────────────────────────────────────
@main.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        rating = request.form.get('rating', '0')

        if not message:
            flash('Please enter a message.', 'error')
        elif not rating.isdigit() or int(rating) not in range(1, 6):
            flash('Please select a rating between 1 and 5.', 'error')
        else:
            fb = Feedback(user_id=current_user.id, message=message, rating=int(rating))
            db.session.add(fb)
            db.session.commit()
            flash('Thanks for your feedback!', 'success')
            return redirect(url_for('main.feedback'))

    return render_template('feedback.html')


# ──────────────────────────────────────
# Email verification
# ──────────────────────────────────────
@main.route('/verification-sent')
def verification_sent():
    email = request.args.get('email', '')
    return render_template('verification_sent.html', email=email)


@main.route('/verify/<token>')
def verify_email(token):
    email = verify_token(token, salt='email-verify', max_age=3600)
    if not email:
        flash('Verification link is invalid or has expired. Please request a new one.', 'error')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('No account found for this email.', 'error')
        return redirect(url_for('main.register'))

    if user.email_verified:
        flash('Your email is already verified. Please log in.', 'success')
        return redirect(url_for('main.login'))

    user.email_verified = True
    db.session.commit()
    flash('Email verified successfully! You can now log in.', 'success')
    return redirect(url_for('main.login'))


@main.route('/resend-verification', methods=['POST'])
def resend_verification():
    email = request.form.get('email', '').strip()
    user = User.query.filter_by(email=email).first()

    # Always show the same message (don't leak whether an email is registered)
    if user and not user.email_verified:
        send_verification_email(user)

    flash('If an unverified account exists for that email, a new verification link has been sent.', 'success')
    return redirect(url_for('main.verification_sent', email=email))


# ──────────────────────────────────────
# Forgot password / Reset password
# ──────────────────────────────────────
@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = User.query.filter_by(email=email).first()

        # Always respond the same way to prevent email enumeration
        if user:
            send_password_reset_email(user)

        flash(
            'If an account exists for that email, a password reset link has been sent. '
            'The link expires in 1 hour.',
            'success'
        )
        return redirect(url_for('main.login'))

    return render_template('forgot_password.html')


@main.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    email = verify_token(token, salt='password-reset', max_age=3600)
    if not email:
        flash('Reset link is invalid or has expired. Please request a new one.', 'error')
        return redirect(url_for('main.forgot_password'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('No account found for this email.', 'error')
        return redirect(url_for('main.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not password or len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return redirect(url_for('main.reset_password', token=token))

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('main.reset_password', token=token))

        if user.check_password(password):
            flash('New password cannot be the same as your old password.', 'error')
            return redirect(url_for('main.reset_password', token=token))

        user.set_password(password)
        # A password reset also implicitly verifies ownership of the email
        user.email_verified = True
        db.session.commit()

        flash('Password reset successfully! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('reset_password.html', token=token)



# --- 1. ADMIN DASHBOARD ---

@main.route('/admin')
@login_required
def admin_dashboard():
    ADMIN_EMAIL = 'legendofwinning002@gmail.com'

    if current_user.email.strip().lower() != ADMIN_EMAIL.strip().lower():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.home'))

    from app.models import User, Attempt, Feedback
    from sqlalchemy import func

    total_users = User.query.count()
    total_attempts = Attempt.query.count()
    total_feedback = Feedback.query.count()

    # Average rating (rounded to 1 decimal)
    avg = db.session.query(func.avg(Feedback.rating)).scalar()
    avg_rating = round(avg, 1) if avg else '—'

    users = User.query.order_by(User.created_at.desc()).all()
    feedback_list = Feedback.query.order_by(Feedback.timestamp.desc()).all()

    return render_template('admin.html',
                           total_users=total_users,
                           total_attempts=total_attempts,
                           total_feedback=total_feedback,
                           avg_rating=avg_rating,
                           users=users,
                           feedback_list=feedback_list)


# --- 2. CSV EXPORT ---


@main.route('/attempts/export')
@login_required
def export_attempts():
    """Download all of the current user's attempts as a CSV file."""
    from app.models import Attempt
    import csv
    import io

    attempts = Attempt.query.filter_by(user_id=current_user.id) \
        .order_by(Attempt.timestamp.desc()).all()

    # Build CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['#', 'Type', 'Input', 'Result', 'Date'])

    for i, a in enumerate(attempts, 1):
        writer.writerow([
            i,
            a.input_type,
            a.input_value,
            a.result,
            a.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])

    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=armstrong_attempts.csv'
        }
    )
    return response
