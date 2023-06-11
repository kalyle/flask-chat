import click
from flask.cli import FlaskGroup

from app import create_app

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
if __name__ == '__main__':
    cli()



