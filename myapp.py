from app import create_app, socketio

#Calls function from the app init page that wraps the app in all needed functionality
app = create_app()

if __name__ == '__main__':
    socketio.run(app)