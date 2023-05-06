from app.user import bp
from flask import render_template
from flask_login import current_user, login_required

from .. import db
from ..models import User


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = db.session.query(User).filter(User.id == current_user.id).first()
    return render_template('user/profile.html', user=user)
