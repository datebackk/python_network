import os


class Config:
    DEBUG_MODE = os.environ.get('DEBUG_MODE') or True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'youNeverGuessIT'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
