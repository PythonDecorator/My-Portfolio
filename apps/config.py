import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """The Config layout class contains settings that are common to all configurations; the different subclasses define
      settings that are specific to a configuration. Additional configurations can be added as needed"""

    # SECRET_KEY, due to its sensitive nature, can be set in the environment,
    # but a default value is provided in case the environment does not define it.
    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT')

    SOCIAL_AUTH_GITHUB = False

    GITHUB_ID = os.getenv('GITHUB_ID')
    GITHUB_SECRET = os.getenv('GITHUB_SECRET')

    # Enable/Disable GitHub Social Login
    if GITHUB_ID and GITHUB_SECRET:
        SOCIAL_AUTH_GITHUB = True


class DevelopmentConfig(Config):
    """ This enables the application to run under different configurations, each using a different database."""
    DEBUG = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

    # # Using the data directly. Not recommended.
    # This will create a file in <apps> folder.
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_test.sqlite3')


class ProductionConfig(Config):
    """For production debug is not used, and it is recommended to use PostgresSQL database"""
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgresSQL database
    # SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
    #     os.getenv('DB_ENGINE'),
    #     os.getenv('DB_USERNAME'),
    #     os.getenv('DB_PASS'),
    #     os.getenv('DB_HOST'),
    #     os.getenv('DB_PORT'),
    #     os.getenv('DB_NAME')
    # )

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')


# The different configurations of the script are registered in a config dictionary.
config_dict = {
    'Production': ProductionConfig,
    'Debug': DevelopmentConfig
}
