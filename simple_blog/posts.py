import re
from flask import Blueprint, render_template, request, redirect, url_for
from simple_blog.db import get_db
from simple_blog.auth import login_required

bp = Blueprint("posts", __name__, url_prefix="/posts")


def slugify(title):
    title = title.replace("'", "")
    return re.sub(r'[\W_]+', '-', title.lower())


@bp.route("/<string:slug>", methods=("GET",))
def post(slug):
    db = get_db()
    post = db.execute(
        "SELECT * FROM posts WHERE slug = ?", (slug,)
    ).fetchone()

    if post is None:
        return render_template("posts/notfound.html")

    return render_template("posts/post.html", post=post)

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        slug = slugify(title)
        body = request.form["body"]
        error = None
        
        if not title or not body:
            error = "Must enter both title and body"
        else:
            db = get_db()
            db.execute(
                "INSERT INTO posts (title, body, slug) VALUES (?, ?, ?)",
                (title, body, slug)
            )
            db.commit()
            
            return redirect(url_for("home"))

    return render_template("posts/create.html")


