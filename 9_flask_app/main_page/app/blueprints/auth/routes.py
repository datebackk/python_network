from app.blueprints.auth import auth
from app.database import db
from app.database.models.user import User
from datetime import datetime
from flask import render_template, url_for, redirect, request, jsonify, flash, current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.security import check_password_hash


@auth.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        user = User.query.filter(User.email == email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=request.form.get('remember'))
            return redirect(url_for('auth.index'))

        flash('Неправильный логин или пароль')
        return render_template('login.html')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        check_email = User.query.filter(User.email == email).first()

        if check_email:
            flash('Пользователь с таким email уже существует')
            return render_template('register.html')

        user = User(
            password=generate_password_hash(password),
            email=email,
            date_of_registration=datetime.utcnow(),
        )

        db.session.add(user)
        db.session.flush()
        db.session.commit()

        login_user(user)

        return redirect(url_for('auth.index'))

    return render_template('register.html')


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
