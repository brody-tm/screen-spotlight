from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name=None):
    app = Flask(__name__)

    # Apply configuration
    if config_name:
        app.config.from_object(config_name)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints (modular routing)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import models so db.create_all() knows about them
    from . import models

    return app