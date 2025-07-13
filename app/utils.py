# app/utils.py

from flask import request, current_app

def get_locale():
    return request.accept_languages.best_match(current_app.config['APP_LANGUAGES'])


def print_console(msg):
    print(f" --> [microblog] {(msg.strip())}")


