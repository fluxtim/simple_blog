import os
import tempfile
import pytest
from simple_blog import create_app
from simple_blog.db import init_db, get_db
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        db = get_db()
        db.execute(
            "INSERT INTO users (username, handle, userpass) VALUES (?, ?, ?)",
            ('test', 'test', generate_password_hash('test'))
        )
        db.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', userpass='test'):
        self._client.post(
            '/auth/login',
            data={'username':username, 'userpass':userpass}
        )

    def logout(self):
        self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)