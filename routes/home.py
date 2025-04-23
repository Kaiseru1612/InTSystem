from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.course import Course
from services.ai_model import AIModel  # Import AI model class
from services.recommendation_service import *

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if current_user.is_authenticated:
        saved_courses = Course.query.filter_by(user_id=current_user.id).all()
        recommended_courses = generate_recommendations(saved_courses)
        return render_template('app.html', saved_courses=saved_courses, recommended_courses = recommended_courses, user=current_user)
    else:
        return redirect(url_for('auth.login'))

@home_bp.route('/about')
def about():
    return render_template('about.html')
