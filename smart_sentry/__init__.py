from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from smart_sentry.config import Config

# Setup Flask-MongoEngine
db = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    """ Flask application factory """

    # Setup Flask and load app.config
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask-MongoEngine
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from smart_sentry.users.routes import users
    from smart_sentry.main.routes import main
    from smart_sentry.errors.handlers import errors
    from smart_sentry.ml_api.routes import ml_api
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(ml_api)

    return app
