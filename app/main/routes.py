from flask import render_template
from app.main import bp

@bp.route("/")
@bp.route("/index")
def index():
    contex = {'user': {'username': 'jnya'},
              'title': 'Hillel'
              }
    return render_template("index.html", **contex)


@bp.route("/about")
def about():
    contex = {'user': {'username': 'jnya'},
              'title': 'About us'
              }
    return render_template("about.html", **contex)





