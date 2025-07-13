# app/main/__init__.py : package with the core of the application

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import forms, routes

