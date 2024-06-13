from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask import render_template

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventdata.db'
    db.init_app(app)
    Bootstrap5(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .views import mainbp
    app.register_blueprint(mainbp)

    from .auth import authbp
    app.register_blueprint(authbp)

    from .events import destbp as events_blueprint
    app.register_blueprint(events_blueprint)

    #404 Not Found Error Handler
    @app.errorhandler(404)
    def not_found_error(error):
            return render_template('error.html', error_code=404, error_message="Page not found"), 404

    #403 Forbidden Error Handler
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('error.html', error_code=403, error_message="Access forbidden"), 403

    #500 Internal Server Error Handler
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('error.html', error_code=500, error_message="Internal server error"), 500

    #502 Bad Gateway Error Handler
    @app.errorhandler(502)
    def bad_gateway_error(error):
        return render_template('error.html', error_code=502, error_message="Bad gateway"), 502

    #504 Gateway Timeout Error Handler
    @app.errorhandler(504)
    def gateway_timeout_error(error):
        return render_template('error.html', error_code=504, error_message="Gateway timeout"), 504

    #General Error Handler
    @app.errorhandler(Exception)
    def unhandled_exception(error):
        return render_template('error.html', error_code=500, error_message="Internal server error"), 500

    return app
