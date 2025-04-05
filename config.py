import os

class Config:
    SECRET_KEY = os.environ.get('qsef82esq2', 'zscf1b6vxf1')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
