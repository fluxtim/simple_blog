from flask import Flask, render_template, request
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping({
        "SECRET_KEY": "DEV",
        "DATABASE": os.path.join(app.instance_path, "passingdb.sqlite") 
    })

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=("GET",))
    def home():
        if request.method == "GET":
            posts = db.get_db().execute(
                "SELECT * FROM posts"
            ).fetchall()

            return render_template("home.html", posts=posts)
    
    from . import posts
    app.register_blueprint(posts.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import db
    db.init_app(app)

    return app