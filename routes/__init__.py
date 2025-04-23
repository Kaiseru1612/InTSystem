# routes/__init__.py
from flask import Blueprint

def register_routes(app):
    # Import blueprints inside the function to avoid circular imports
    from .auth import auth_bp
    from .course import course_bp
    from .dashboard import dashboard_bp
    from .quiz import quiz_bp
    from .home import home_bp
    
    # Register blueprints with specific URL prefixes
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(course_bp, url_prefix='/course')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(home_bp)  
