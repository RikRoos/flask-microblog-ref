# app/auth/email.py : email functionality for authentication

from flask import render_template, current_app
from app.email import send_email

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(subject='[Microblog] Reset Your Password',
               sender=current_app.config['SECRETS_MAIL_ADMINS'][0],       #TODO: make special sender
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', 
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html', 
                                         user=user, token=token))

