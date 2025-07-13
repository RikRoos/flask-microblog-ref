# app/auth/__init__.py : a blueprint package for dealing with authentication

from flask import Blueprint


bp = Blueprint('authentication', __name__, template_folder='templates', static_folder='static', url_prefix='/auth')


from app.auth import forms, routes
