from simple_blog.db import get_db

def test_auth(client, app):
    assert client.get('/auth/login').status_code == 200

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM users WHERE username = 'test'"
        ).fetchone() is not None

def test_pages(client, auth):
    auth.login()
    response = client.get('/posts/create')
    assert b"Create post page" in response.data