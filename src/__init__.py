from flask import Flask
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

# Initialize Flask Extensions
db =  SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

# Initialize logging based on the environment
def setup_logging(app):
    """Setup app logging"""
    log_level = logging.INFO
    if app.config['ENV'] == 'production':
        log_level = logging.WARNING
    
    # Create the logs directory if it does not exist    
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir) 
    
    # Define the path for the log file
    log_file_path = os.path.join(logs_dir, 'application.log')
    
    # Create a file handler for outputting logs
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    app.logger.setLevel(log_level)
    
    # Set up a stream handler with a higher log level
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(log_level)


def create_app():
    """Create and configure and instance of the Flask application."""
    app = Flask(__name__)
    
    # Load environment specific configurations
    env = os.environ.get('FLASK_ENV', 'development')
    if env =='production':
        from src.config.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from src.config.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Set up logging
    setup_logging(app)
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    
    # Register Blueprints
    from src.blueprints.auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    return app