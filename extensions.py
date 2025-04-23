# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize these objects here
db = SQLAlchemy()
login_manager = LoginManager()
