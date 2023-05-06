import click
from app.models import User, Profile
from flask import Blueprint
from faker import Faker
from app import db

bp = Blueprint('fake', __name__)
faker = Faker()


@bp.cli.command("users")
@click.argument('num', type=int)
def users(num):
    """
    Create 'num' of fake users
    """
    users = []
    for i in range(num):
        # generate fake username
        username = faker.user_name()

        # generate fake email
        email = faker.email()

        # generate fake password
        password = faker.password()

        # generate fake first_name
        first_name = faker.first_name()

        # generate fake last_name
        last_name = faker.last_name()

        # get user by username & email
        user = (
            db.session.query(User)
            .filter(
                User.username == username,
                User.email == email,

            )
        ).first()
        # no such user in db yet --> insert
        if not user:
            user = User(
                username=username,
                email=email,
                password=password
            )
            user.set_password(password)
            db.session.add(user)
            users.append(user)
            db.session.commit()
        profile = Profile(user_id=user.id, first_name=first_name,
                          last_name=last_name,
                          bio="Lorem ipsum dolor sit amet, ",
                          linkidln_link=f"https://facebook.com/{user.username}",
                          facebook_link=f"https://linkied.com/{user.username}"
                          )
        db.session.add(profile)
        # persist changes
        db.session.commit()
    print(num, 'users added.')
