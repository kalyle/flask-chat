import click
from app import create_app
from app.api.chat import NotifyNamespace, ChatNamespace
from app.extensions.init_ext import socketio


@click.command()
@click.option('-p', default=8000, help='run with socketio')
def runserver(p):
    app = create_app()

    socketio.init_app(app)
    socketio.on_namespace(NotifyNamespace('/notify'))
    socketio.on_namespace(ChatNamespace('/chat'))
    socketio.run(app, port=p)


if __name__ == '__main__':
    runserver()
