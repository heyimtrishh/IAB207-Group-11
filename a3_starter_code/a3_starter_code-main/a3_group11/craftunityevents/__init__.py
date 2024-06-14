from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
import logging

# Initialize the database object
db = SQLAlchemy()

def create_app():
    # Create an instance of the Flask class
    app = Flask(__name__)
    app.debug = True
    
    # Configure the upload folder for images
    UPLOAD_FOLDER = '\static\image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    # Set the secret key for session management and other security-related needs
    app.secret_key = 'somesecretkey'
    
    # Configure the SQLAlchemy part of the app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventdata.db'
    
    # Initialize the database object with the settings above
    db.init_app(app)
    
    # Initialize Bootstrap5 for the app
    Bootstrap5(app)

    # Setup Flask-Login for user session management
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the login view
    login_manager.init_app(app)

    # Import the User model for the user loader callback
    from .models import User
    
    # Define the user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register the main blueprint
    from .views import mainbp
    app.register_blueprint(mainbp, url_prefix='/')

    # Import and register the authentication blueprint
    from .auth import authbp
    app.register_blueprint(authbp, url_prefix='/auth')

    # Import and register the events blueprint
    from .events import destbp as events_blueprint
    app.register_blueprint(events_blueprint, url_prefix='/events')

    # Define error handlers for different HTTP error codes

    # 404 Not Found Error Handler
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', error_code=404, error_message="Page not found"), 404

    # 403 Forbidden Error Handler
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('error.html', error_code=403, error_message="Access forbidden"), 403

    # 500 Internal Server Error Handler
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('error.html', error_code=500, error_message="Internal server error"), 500

    # 502 Bad Gateway Error Handler
    @app.errorhandler(502)
    def bad_gateway_error(error):
        return render_template('error.html', error_code=502, error_message="Bad gateway"), 502

    # 504 Gateway Timeout Error Handler
    @app.errorhandler(504)
    def gateway_timeout_error(error):
        return render_template('error.html', error_code=504, error_message="Gateway timeout"), 504

    # General Error Handler for uncaught exceptions
    @app.errorhandler(Exception)
    def unhandled_exception(error):
        return render_template('error.html', error_code=500, error_message="Internal server error"), 500

    return app
