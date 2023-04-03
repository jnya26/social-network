from app import db
from flask import render_template
from app.main import bp
from app.models import User


@bp.route("/")
@bp.route("/index")
def index():

    users_data = [
        {
            "username": "akushyn",
            "email": "akushyn@gmail.com",

        },
        {
            "username": "anton",
            "email": "antonn@gmail.com",

        },
        {
            "username": "denys",
            "email": "denys@gmail.com",

        },
        {
            "username": "tanya",
            "email": "tanya@gmail.com",

        },
        {
            "username": "igor",
            "email": "igor@gmail.com",

        },
    ]

    for u in users_data:
        user = (
            db.session.query(User)
            .filter(
                User.username == u.get('username'),
                User.email == u.get('email'),
            ).first()
        )
        if user:
            continue

        user = User(
            username=u.get('username'),
            email=u.get('email'),
            password=u.get('password')
        )
        db.session.add(user)
    db.session.commit()

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





