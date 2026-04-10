from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Please log in to access this page.'


def create_app():
    app = Flask(__name__)

    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'change-this-to-a-random-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'armstrong.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    # Create database tables
    with app.app_context():
        from app import models
        db.create_all()

    return app