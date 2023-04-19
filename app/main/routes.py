from app import db
from flask import render_template
from app.main import bp
from app.models import User


@bp.route("/")
@bp.route("/index")
def index():
    users_query = db.session.query(User)
    users = users_query.all()
    print(users)
    return render_template("index.html", users=users)


@bp.route("/about")
def about():
    contex = {'user': {'username': 'jnya'},
              'title': 'About us'
              }
    return render_template("about.html", **contex)
