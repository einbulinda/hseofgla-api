import os

class ProductionConfig:
    ENV = "production"
    DEBUG = False
    PORT = 80
    HOST = '0.0.0.0'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    
