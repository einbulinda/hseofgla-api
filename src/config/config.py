from src.config.dev_config import DevConfig
from src.config.production import ProductionConfig
import os

class Config:
    # Common environment configurations
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT')

class DevelopmentConfig(Config, DevConfig):
    pass

class ProductionConfig(Config,ProductionConfig):
    pass
