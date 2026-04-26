from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail # For sending emails (e.g., feedback notifications)
from dotenv import load_dotenv # For loading environment variables from a .env file
import os # For environment variable handling

load_dotenv() # Load environment variables from .env file
 
 #not connected to the database yet, just setting up the extension
db = SQLAlchemy()  # Initialize SQLAlchemy
login_manager = LoginManager() # Initialize Flask-Login
login_manager.login_view = 'main.login'  #if someone isn't logged in and they try to get to th e dashboard, they will be redirected to the login page
login_manager.login_message = 'Please log in to access this page.'
mail = Mail() # Initialize Flask-Mail


def create_app():
    app = Flask(__name__)

    # Core config
    basedir = os.path.abspath(os.path.dirname(__file__)) # Get the absolute path of the directory where this file is located
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-fallback-key-change-me') # Use an environment variable for the secret key, with a fallback for development
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, '..', 'armstrong.db')
    ) # Use an environment variable for the database URI, with a fallback to a local SQLite database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # turn off the Flask-SQLAlchemy event system, which is not needed and can consume extra resources

    # Mail config (Gmail SMTP by default)
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv(
        'MAIL_DEFAULT_SENDER',
        app.config['MAIL_USERNAME']
    )

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app) # Initialize Flask-Mail with the app's mail configuration

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    # Create database tables
    # Tells flask "we're ready to work with the database, so please create the tables if they don't exist yet"
    with app.app_context():
        from app import models
        db.create_all()

    return app
