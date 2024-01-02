import sqlite3
from flask import g, current_app
import click
from werkzeug.security import generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    db.execute(
        "INSERT INTO posts (title, body, slug) VALUES (?, ?, ?)",
        ("Test post 1", "The body of the post called test post 1", "test-post-1")
    )
    db.execute(
        "INSERT INTO posts (title, body, slug) VALUES (?, ?, ?)",
        ("Test post 2", "The body of the post called test post 2", "test-post-2")
    )
    db.execute(
        "INSERT INTO users(username, handle, userpass) VALUES (?, ?, ?)",
        ("tim", "Tim", generate_password_hash("timpass") )
    )
    db.commit()


@click.command('init-db')
def init_db_command():
    """Initialised the dev database"""
    init_db()
    click.echo("Initialised the dev database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    