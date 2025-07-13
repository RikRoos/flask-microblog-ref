# app/routes.py
from datetime import datetime, timezone

from urllib.parse import urlsplit
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm
from app.auth.forms import RegistrationForm
from app.auth.forms import ResetPasswordRequestForm
from app.auth.forms import ResetPasswordForm
from app.auth.email import send_password_reset_email

#----------------------------------------------------------------------
# VIEW : LOGIN
#----------------------------------------------------------------------

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('authentication.login'))
        login_user(user, remember=form.remember_me.data)  # this will register the user as logged in
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#----------------------------------------------------------------------
# VIEW : LOGOUT
#----------------------------------------------------------------------

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

#----------------------------------------------------------------------
# VIEW : REGISTER
#----------------------------------------------------------------------

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a regsitered user!')
        return redirect(url_for('authentication.login'))
    return render_template('register.html', title='Register', form=form)

#----------------------------------------------------------------------
# VIEW : RESET_PASSWORD_REQUEST
#----------------------------------------------------------------------

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
         return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        # always flash the message to obscure the presence of a mail address
        flash(f'Check your email for instructions to reset your password.')
        return redirect(url_for('authentication.login'))
    # processing the inital GET request:
    return render_template('reset_password_request.html', 
                           title='Reset Password', form=form)

#----------------------------------------------------------------------
# VIEW : RESET_PASSWORD/<TOKE>
#----------------------------------------------------------------------

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    The user has clicked the URL in the mail with the reset-token. 
    That user action will cause a get-request for this view. If the returned 
    token is valid the user will be presented a form to enter his/her new 
    password.
    """
    if current_user.is_authenticated:
         return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        # maybe the token has been tampered
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # this is during the POST-action after entering a new password
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('authentication.login'))
    # during GET-request: serve the form to enter a new password
    return render_template('reset_password.html', form=form)

