import os

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'YOLO'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') \
        or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFIFACTIONS = False