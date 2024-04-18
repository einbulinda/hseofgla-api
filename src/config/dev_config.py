import os

class DevConfig:
    ENV = "development"
    DEBUG = True
    PORT = 3000
    HOST = '0.0.0.0'
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')

