from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5

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
    app.register_blueprint(mainbp, url_prefix='/')

    from .auth import authbp
    app.register_blueprint(authbp, url_prefix='/auth')

    from .events import destbp as events_blueprint
    app.register_blueprint(events_blueprint, url_prefix='/events')

    return app
