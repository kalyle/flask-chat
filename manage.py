import click
from app import create_app
from app.api.chat import NotifyNamespace, ChatNamespace
from app.extensions.init_ext import socketio


@click.command()
@click.option('-h', default="127.0.0.1", help='run host with socketio')
@click.option('-p', default=8000, help='run port with socketio')
def runserver(h, p):
    app = create_app()

    socketio.init_app(app)
    socketio.on_namespace(NotifyNamespace('/notify'))
    socketio.on_namespace(ChatNamespace('/chat'))
    socketio.run(app, host=h, port=p)


if __name__ == '__main__':
    runserver()
