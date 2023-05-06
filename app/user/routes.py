from app import db
from app.models import Posts, User, Follow, Activities
from app.post.forms import CreatPost
from app.user import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.user.forms import ProfileForm, EditPasswordForm

from ..services import UserService

user_service = UserService()


@bp.route("/blog")
@login_required
def blog():
    form = CreatPost()
    posts = db.session.query(Posts).filter(Posts.autor_id == current_user.id).order_by(Posts.created_at.desc()).all()
    print(posts)
    return render_template("user/blog.html", posts=posts, form=form)


@bp.route("/profile/<string:username>", methods=["GET", "POST"])
@login_required
def profile(username):
    user = db.session.query(User).filter(User.username == username).first_or_404()
    form = ProfileForm()
    result = ''

    if form.validate_on_submit():
        fields = {
            'country': user.profile.country,
            'last_name': user.profile.last_name,
            'first_name': user.profile.first_name,
            'facebook_link': user.profile.facebook_link,
            'linkidln_link': user.profile.linkidln_link,
            'bio': user.profile.bio,
        }

        for field, value in fields.items():
            if len(getattr(form, field).data) == 0:
                setattr(form, field, value)
            else:
                setattr(user.profile, field, getattr(form, field).data)
        if user.profile.first_name != "To be update" and current_user.profile.first_name != "To be update":
            activity = Activities(
                action=f"{current_user.profile.first_name} {current_user.profile.last_name} Change Profile info ",
                autor_id=current_user.id)
        else:
            activity = Activities(action=f"{current_user.username} Change Profile info ",
                                  autor_id=current_user.id)

        db.session.add(activity)
        db.session.commit()
        flash("Your profile successfully updated.", category='success')

        return redirect(url_for('user.profile', username=user.username))
    formy = EditPasswordForm()
    if formy.validate_on_submit():
        user.password = formy.password.data
        db.session.commit()
        flash("Your  successfully changed your password.", category='success')
    elif request.method == 'GET':
        form.country.data = user.profile.country
        form.last_name.data = user.profile.last_name
        form.bio.data = user.profile.bio
        form.first_name.data = user.profile.first_name
        form.facebook_link.data = user.profile.facebook_link
        form.linkidln_link.data = user.profile.linkidln_link

    following = db.session.query(Follow).filter(Follow.follower_id == user.profile.user_id).all()
    followers = db.session.query(Follow).filter(Follow.followee_id == user.profile.user_id).all()
    posts = db.session.query(Posts).filter(Posts.autor_id == user.id).order_by(Posts.created_at.desc()).all()
    acts = db.session.query(Activities).filter(Activities.autor_id == user.id).order_by(
        Activities.created_at.desc()).all()
    total_likes = 0
    for post in posts:
        total_likes += len(post.likes)
    total_dislikes = 0
    for post in posts:
        total_dislikes += len(post.dislikes)
    if request.method == "POST":
        file = request.files.get('file')
        if not file:
            flash('No file uploaded.')
            return redirect(url_for('user.profile', username=user.username))
        result = cloudinary.uploader.upload(file)

        data = result['secure_url']
        user.profile.photo = data
        db.session.commit()
        print(result)

    return render_template('user/profile.html', user=user, form=form, followers=followers, following=following,
                           posts=posts, total_likes=total_likes, total_dislikes=total_dislikes, acts=acts,
                           cloudinary=cloudinary,
                           result=result, formy=formy)


@bp.route("/<int:user_id>/follow", methods=['GET', 'POST'])
@login_required
def follow(user_id):
    follower = Follow(followee_id=user_id, follower_id=current_user.id)
    db.session.add(follower)
    followers = User.query.get(user_id)
    print(followers.profile.last_name)
    print(current_user.profile.last_name)

    if followers.profile.last_name != "To be update" and current_user.profile.last_name != "To be update":

        activity = Activities(
            action=f"{current_user.profile.first_name} {current_user.profile.last_name} Followed on  "
                   f"{followers.profile.first_name} {followers.profile.last_name}",
            autor_id=current_user.id)
        activity.action = activity.action.encode('utf-8').decode('latin-1')
    else:
        activity = Activities(action=f"{current_user.username} followed on {followers.username} ",
                              autor_id=current_user.id)

    db.session.add(activity)
    db.session.commit()
    flash("You subscribe on this profile", category="success")
    return redirect(request.referrer)


@bp.route("/<int:user_id>/unfollow", methods=['GET', 'POST'])
@login_required
def unfollow(user_id):
    follower = db.session.query(Follow).filter_by(followee_id=user_id).first()
    db.session.delete(follower)
    db.session.commit()
    flash("You unfollow from this profile", category="success")
    return redirect(request.referrer)
