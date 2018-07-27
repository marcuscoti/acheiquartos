from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """
    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///rooms.sqlite'    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com'
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'

    # Flask-User settings
    USER_APP_NAME = "Achei Quartos"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
    USER_SEND_REGISTERED_EMAIL = False
    USER_SEND_PASSWORD_CHANGED_EMAIL = False
    USER_SEND_USERNAME_CHANGED_EMAIL = False
    USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = True
    USER_CHANGE_PASSWORD_TEMPLATE = 'user/change_password.html'
    USER_LOGIN_TEMPLATE = 'user/login.html'
    USER_REGISTER_TEMPLATE = 'user/register.html'
    USER_RESET_PASSWORD_TEMPLATE = 'user/reset_password.html'
    USER_FORGOT_PASSWORD_TEMPLATE = 'user/forgot_password.html'


# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

# Initialize Flask-SQLAlchemy
db = SQLAlchemy(app)

# Setup Flask-Admin
admin = Admin(app, name='Admin', template_mode='bootstrap3')