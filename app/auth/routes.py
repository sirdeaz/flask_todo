from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.auth import bp
from app.extensions import db
from app.models.user import User

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if not email or not password:
        flash('All fields are required.', 'error')
        return redirect(url_for('auth.login'))

    user = db.session.query(User).filter_by(email=email).first()

    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'error')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))

@bp.route('/signup')
def signup():
    return render_template('signup.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    if not email or not first_name or not last_name or not password:
        flash('All fields are required.', 'error')
        return redirect(url_for('auth.signup'))

    user = db.session.query(User).filter_by(email=email).first()

    if user:
        flash('Email already exists.', 'error')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    db.session.add(new_user)
    db.session.commit()

    flash('Account created, please login.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))