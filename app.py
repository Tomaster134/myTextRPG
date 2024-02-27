from app import create_app, socketio
from gevent.pywsgi import WSGIServer

app = create_app()

if __name__ == '__main__':
    socketio.run(app)