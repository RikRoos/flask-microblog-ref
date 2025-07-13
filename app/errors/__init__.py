# app/errors/__init__.html : an error-handling blueprint package

from flask import Blueprint
bp = Blueprint('errors', __name__, template_folder='templates', static_folder='static')

from app.errors import handlers
