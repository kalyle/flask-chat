from app import create_app
from app.api.chat import NotifyNamespace, ChatNamespace
from app.extensions.init_ext import socketio
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', "--host", default="127.0.0.1")
@click.option('-p', "--port", default=8000)
def runserver(host, port):
    app = create_app()

    socketio.init_app(app)
    socketio.on_namespace(NotifyNamespace('/'))
    socketio.on_namespace(ChatNamespace('/chat'))
    socketio.run(app, host=host, port=port, use_reloader=False)


if __name__ == "__main__":
    cli()
