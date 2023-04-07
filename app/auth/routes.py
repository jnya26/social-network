from app.auth import bp
from flask import render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user

from .. import db
from ..models import User, Profile


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Login view function
    """

    # create LoginForm object
    form = LoginForm()

    # validate form on "POST" request
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid password or email", category="error")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember.data)
        # redirect to home page
        return redirect(url_for("user.profile"))

    # render 'login.html' template with passed form
    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("app.user.profile"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)

        user.set_password(form.password.data)

        if User.query.filter_by(username=form.username.data).first():
            flash("User with such username have already registred", category="error")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(email=form.email.data).first():
            flash("User with such email have already registred", category="error")
            return redirect(url_for("auth.register"))

        db.session.add(user)
        db.session.commit()
        profiles = Profile(first_name="To be update", last_name="To be update",
                           linkidln_link="To be update", facebook_link="To be update",
                           user_id=user.id)
        db.session.add(profiles)
        db.session.commit()
        flash("Successfully registered", category="success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
