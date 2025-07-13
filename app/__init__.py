# app/__init__.py : the application package module
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from config import Config
from elasticsearch import Elasticsearch
from app.utils import print_console

# creating the extension instances
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
moment = Moment()
login.login_view = 'authentication.login'           # the endpoint-name of the login function


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # init the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    # register the blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.elasticsearch = Elasticsearch(app.config.get('SECRETS_ELASTICSEARCH_URL', None)) \
                            if app.config.get('SECRETS_ELASTICSEARCH_URL', None) else None

    # adding log handlers:
    if not app.debug and not app.testing and app.config['MAIL_ENABLED']:
        # send email when errors are reported
        auth = None
        if app.config['SECRETS_MAIL_USERNAME'] or app.config['SECRETS_MAIL_PASSWORD']:
           auth = app.config['SECRETS_MAIL_USERNAME'], app.config['SECRETS_MAIL_PASSWORD']
        secure = None
        if app.config['SECRETS_MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(mailhost=(app.config['SECRETS_MAIL_SERVER'], app.config['SECRETS_MAIL_PORT']),
                                   fromaddr=f"no-reply@{app.config['SECRETS_MAIL_SERVER']}",
                                   toaddrs=app.config['SECRETS_MAIL_ADMINS'],
                                   subject="Microblog failure",
                                   credentials=auth,
                                   secure=secure,
                                  )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    else:
        print_console("mail is disbaled by config-setting, debugging or testing")

    # write rotating logfile
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', 
                                       maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

    return app

from app import models


if __name__ == '__main__':
    # start the initialization 
    init_config(*sys.argv[1:])
