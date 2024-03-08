# Required to have my webserver play nicely
from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO
from config import Config
from flask_login import LoginManager
from app.models import db, User
from flask_migrate import Migrate
import logging

#Creates a server object that is used to wrap the app for websocket functionality
socketio = SocketIO()

#function that gets called when flask app is built
def create_app():
    logging.basicConfig(filename='record.log', level=logging.DEBUG) #Includes logging functionality
    app = Flask(__name__)
    app.config.from_object(Config) #Loading in config file

    login_manager = LoginManager() 
    
    login_manager.init_app(app) #Adds login functionality to app
    db.init_app(app) #Adds PostgreSQL functionality to app
    migrate = Migrate(app, db)
    
    #Adds login authentication and redirect functionality
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Ya gotta be logged in to see that, bubs.'
    login_manager.login_message_category = 'warning'

    #Importing blueprints
    from app.blueprints.main import main, events, commands, objects
    from app.blueprints.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    #Adds current_user to global variables
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    #More logging stuff
    @app.route('/logs')
    def logs():
        # showing different logging levels
        app.app.logger.debug("debug log info")
        app.app.logger.info("Info log information")
        app.app.logger.warning("Warning log info")
        app.app.logger.error("Error log info")
        app.app.logger.critical("Critical log info")
        return "testing logging levels."

    #Wraps app in websocket functionality
    socketio.init_app(app)
    return app