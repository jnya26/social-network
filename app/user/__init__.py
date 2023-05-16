from flask import Blueprint
from sqlalchemy import func
from pathlib import Path
from .. import db
import pandas as pd
from ..models import User, Profile, Posts

bp = Blueprint("user", __name__, url_prefix="/user")

from . import routes  # noqa


@bp.cli.command('exctract_users')
def exctract_users():
    user_info = (
        db.session.query(
            User.username,
            User.email,
            Profile.full_name,
            func.count('*').label('Posts Count'))
        .join(Profile, Profile.user_id == User.id)
        .join(Posts, Posts.autor_id == User.id)
        .group_by(User.username, User.email, Profile.full_name).all()
    )
    print(user_info)

    dp = pd.DataFrame(user_info, columns=['Username', 'Email', 'Full name', 'Posts Count'])
    output_file_path = Path(__file__).resolve().parent.parent / 'user_info.csv'
    dp.to_csv(output_file_path, index_label='No')
