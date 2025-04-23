import os

class Config:
    SECRET_KEY = 'alpha-beta-gamma'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
