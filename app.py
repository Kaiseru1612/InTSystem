from http.client import responses

from icecream import ic
from flask import Flask, render_template, request, session, redirect, url_for
from flask import render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import google.generativeai as genai
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import openai  # don't go for upgraded version
import json
import requests
from flask_weasyprint import HTML, render_pdf
from weasyprint import CSS
import models.user
import models.course
from routes.auth import login_manager, auth_bp
from routes.home import home_bp
from routes.course import course_bp
from routes.dashboard import dashboard_bp
from routes.quiz import quiz_bp
from extensions import db

app = Flask(__name__)
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'alpha-beta-gamma'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app) 

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(course_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(quiz_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", debug=True)
