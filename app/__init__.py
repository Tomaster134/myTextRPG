from flask import Flask
from flask_socketio import SocketIO
from config import Config
from flask_login import LoginManager
from app.models import db, User
from flask_migrate import Migrate

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    
    login_manager.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Ya gotta be logged in to see that, bubs.'
    login_manager.login_message_category = 'warning'

    from app.blueprints.main import main
    from app.blueprints.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    socketio.init_app(app)
    return app