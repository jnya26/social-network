from pathlib import Path
import click
import pandas as pd
from flask import Blueprint
from sqlalchemy import func
from .. import db
from ..models import Posts, Like, Dislike

bp = Blueprint("post", __name__, url_prefix="/post")

from . import routes  # noqa


@bp.cli.command('extract_posts')
@click.argument('user_id', type=int)
def extract_posts(user_id):
    user = db.session.query(Posts).filter(Posts.autor_id == user_id).first()
    print(user.author.username)
    if user is None:
        print(f"User with ID {user} does not exist.")
        return

    posts = (
        db.session.query(
            Posts.title,
            func.count(Like.id).label('Likes count'),
            func.count(Dislike.id).label('Dislikes count'),
            Posts.created_at.label('Posts Created')
        )
        .join(Like, Like.post_id == Posts.id, isouter=True)
        .join(Dislike, Dislike.post_id == Posts.id, isouter=True).filter(Posts.autor_id == user_id)
        .group_by(Posts.title, Posts.created_at)
        .all()
    )

    if not posts:
        print(f"No posts found for user {user.author.username}.")
        return
    dp = pd.DataFrame(posts, columns=['Title', 'Likes count', 'Dislikes count', 'Posts Created'])
    dp.index = range(1, len(dp) + 1)
    output_file_path = Path(__file__).resolve().parent.parent / f'{user.author.username}user_info.csv'
    dp.to_csv(output_file_path, index_label='No')

    print(f"Posts for user {user.author.username} have been extracted to {user.author.username}user_info.csv.")
