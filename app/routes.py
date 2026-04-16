from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Attempt, Feedback

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

        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))

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
                    flash('New password cannot be the same as the current password.', 'error')
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