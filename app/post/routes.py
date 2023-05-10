from flask import flash, redirect, request, url_for, render_template, abort
from flask_login import login_required, current_user

from app import db
from app.models import Posts, Like, Dislike, Activities
from app.post import bp
from app.post.forms import CreatPost


@bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = CreatPost()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Posts(content=form.content.data, title=form.title.data, autor_id=current_user.id)

            post.content = form.content.data
            db.session.add(post)
            action_post = Posts.query.get_or_404(current_user.id)
            if action_post.author.profile.first_name != "To be update" and current_user.profile.first_name \
                    != "To be update":
                activity = Activities(
                    action=f"{current_user.profile.first_name} {current_user.profile.last_name} Created post ",
                    autor_id=current_user.id)
            else:
                activity = Activities(action=f"{current_user.username} Created post ",
                                      autor_id=current_user.id)
            db.session.add(activity)
            db.session.commit()
            flash("Your Post successfully added.", category='success')
        else:
            title = form.title.data
            content = form.content.data
            if not title or len(title) < 2:
                flash("Put at least 3 characters in title", category='error')
            if not content or len(content) < 10:
                flash("Put at least 10 characters in content", category='error')
        return redirect(url_for("user.blog"))
    return render_template('user/blog.html', title='Create Post', form=form)


@bp.route("/<int:post_id>/like", methods=['GET', 'POST'])
@login_required
def like(post_id):
    post = Posts.query.get_or_404(post_id)

    if Like.query.filter_by(user=current_user, post=post).count() > 0:
        flash("You have already like it", category="error")
    else:
        dislike = db.session.query(Dislike).filter(Dislike.post_id == post.id).first()
        if dislike:
            db.session.delete(dislike)
        like_post = Like(user=current_user, post=post)
        if post.author.profile.first_name != "To be update" and current_user.profile.first_name != "To be update":
            activity = Activities(
                action=f"{current_user.profile.first_name} {current_user.profile.last_name} liked "
                       f"{post.author.profile.first_name} {post.author.profile.last_name} post",
                autor_id=current_user.id)
        else:
            activity = Activities(action=f"{current_user.username} liked {post.author.username} post",
                                  autor_id=current_user.id)
        db.session.add(like_post)
        db.session.add(activity)
        db.session.commit()
        flash("You like this post", category="success")
    return redirect(request.referrer)


@bp.route("/<int:post_id>/dislike", methods=['GET', 'POST'])
@login_required
def dislike(post_id):
    post = Posts.query.get_or_404(post_id)
    if Dislike.query.filter_by(user=current_user, post=post).count() > 0:
        flash('You have already disliked this post!', category="error")
    else:
        like = db.session.query(Like).filter(Like.post_id == post.id).first()
        if like:
            db.session.delete(like)
        dislike_post = Dislike(user=current_user, post=post)
        if post.author.profile.first_name != "To be update" and current_user.profile.first_name != "To be update":
            activity = Activities(
                action=f"{current_user.profile.first_name} {current_user.profile.last_name} disliked "
                       f"{post.author.profile.first_name} {post.author.profile.last_name} post",
                autor_id=current_user.id)
        else:
            activity = Activities(action=f"{current_user.username} disliked {post.author.username} post",
                                  autor_id=current_user.id)
        db.session.add(dislike_post)
        db.session.add(activity)
        db.session.commit()
        flash("You dislike this post", category="success")

    return redirect(request.referrer)


@bp.route("/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.autor_id != current_user.id:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash("You post successfully delete", category="success")
    return redirect(url_for("user.blog"))
