from flask import Flask
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from src.services.extensions import init_app


# Load environment variables
load_dotenv()

# Initialize logging based on the environment
def setup_logging(app):
    """Setup app logging"""
    log_level = logging.INFO if app.config['ENV'] != 'production' else logging.WARNING
    
    # Create the logs directory if it does not exist    
    logs_dir = os.path.join(os.path.dirname(__file__),app.config.get('LOG_DIR','logs'))
    os.makedirs(logs_dir, exist_ok=True) 
    
    # Define the path for the log file
    log_file_path = os.path.join(logs_dir, app.config.get('LOG_FILE', 'application.log'))
    
    # Create a file handler for outputting logs
    file_handler = RotatingFileHandler(
        log_file_path, 
        maxBytes=app.config.get('LOG_MAX_BYTES',10*1024),
        backupCount=app.config.get('LOG_BACKUP_COUNT',10)
    )
    
    file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)
    
    if app.config['ENV'] != 'production':
        # Set up a stream handler with a higher log level
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    


def create_app():
    """Create and configure and instance of the Flask application."""
    app = Flask(__name__)
    
    # Load environment specific configurations
    env = os.environ.get('FLASK_ENV', 'development')
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    if env =='production':
        from src.config.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from src.config.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Set up logging
    setup_logging(app)
    
    # Initialize extensions
    init_app(app)
    
    
    # Register Blueprints
    from src.blueprints.auth import auth as auth_blueprint
    from src.routes import products as products_blueprint, categories as categories_blueprint
    

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(categories_blueprint)
    
    return app