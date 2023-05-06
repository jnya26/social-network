from app import db
from flask import render_template
from app.main import bp
from app.models import Posts


@bp.route("/")
@bp.route("/index")
def index():
    posts = db.session.query(Posts).order_by(Posts.created_at.desc()).all()
    return render_template("index.html", posts=posts)


@bp.route("/about")
def about():
    contex = {'user': {'username': 'jnya'},
              'title': 'About us'
              }
    return render_template("about.html", **contex)
