import click
from flask.cli import FlaskGroup

from app import create_app
from app.models import db


def create_app_with_config(*args, **kwargs):
    create_app("dev")


@click.group(cls=FlaskGroup, create_app=create_app_with_config)
def cli():
    pass


@cli.command()
def create_all():
    """Creates a database with all of the tables defined in
    your SQLAlchemy models
    """
    # if not database_exists(db.engine.url):
    #     create_database(db.engine.url)

    db.create_all()


@cli.command()
def drop_all():
    """Drop a database with all of the tables defined in
    your SQLAlchemy models
    """

    db.drop_all()


@cli.command(name="show_urls")
def show_urls():
    #
    click.echo('Syncing')
    print("hello")


if __name__ == '__main__':
    cli()



