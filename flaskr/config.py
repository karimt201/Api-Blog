import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:qwerty@localhost:5432/Blog2')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
