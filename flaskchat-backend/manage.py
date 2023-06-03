import click
from flask.cli import FlaskGroup

from app import create_app
from app.models import db


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


# @cli.command()
# def db_create():
#     """Creates database with all of the tables defined in
#     your SQLAlchemy models
#     """
#     db.create_all()


# @cli.command()
# def db_drop():
#     """Drop database with all of the tables defined in
#     your SQLAlchemy models
#     """
#     db.drop_all()

@cli.command()
def hello():
    print("Hello")

@cli.command()
def create():
    db.create_all()

@cli.command()
def drop():
    db.drop_all()
if __name__ == '__main__':
    cli()



