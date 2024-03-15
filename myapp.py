from app import create_app, socketio
from app.blueprints.main.objects import World
import app.blueprints.main.events

#Calls function from the app init page that wraps the app in all needed functionality
app = create_app()

if __name__ == '__main__':
    socketio.run(app)