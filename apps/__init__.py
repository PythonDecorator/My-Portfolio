from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
gravatar = Gravatar(size=100, rating='g', default='retro', force_default=False,
                    force_lower=False, use_ssl=False, base_url=None)


def register_extensions(app):
    """Once an application is created and configured, the extensions can be initialized. Calling init_app()
    and passing the app as an argument"""

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    ckeditor.init_app(app)
    gravatar.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    """This function only create the database model before the first request"""
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    return app
