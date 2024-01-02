from flask import Blueprint, render_template, url_for, redirect, request, session, flash, g
from simple_blog.db import get_db
from werkzeug.security import check_password_hash
import functools

from simple_blog.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        userpass = request.form['userpass']
        error = None

        if not username or not userpass:
            error = "Must enter both username and password"
        
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Username doesn't exist"
        
        elif not check_password_hash(user['userpass'], userpass):
            error = "Incorrct password"
        else:    
            session.clear()
            session['user_id'] = user["id"]
            return redirect(url_for('home'))

        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout", methods=("GET", ))
def logout():
    session.clear()
    return redirect(url_for('home'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def view_wrapper(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return view_wrapper