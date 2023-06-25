import click
from app import create_app
from app.api.chat import NotifyNamespace
from app.extensions.socketio import socketio


@click.command()
@click.option('-p', default=8000, help='run port')
def runserver(p):
    app = create_app()

    socketio.init_app(app)
    socketio.on_namespace(NotifyNamespace('/notify'))
    socketio.run(app, port=p)


if __name__ == '__main__':
    runserver()
