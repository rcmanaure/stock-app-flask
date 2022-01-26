from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from services.forms.forms import UpdateAccountForm, PostForm
from .app import db, app, Post
import os
import secrets
from PIL import Image

main = Blueprint('main', __name__)


@main.route('/')
def publication():
    publications = Post.query.all()
    return render_template('publication.html', publications=publications)


def save_picture(form_picture):
    # To save new profile pic.
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@main.route('/profile', methods=['POST', 'GET'])
@login_required  # Must be log in to see main page.
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    photo = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', name=current_user.email, photo=photo, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.publication'))
    return render_template('create_post.html', form=form, legend='New Publication')


@app.route("/post/<int:id>")
def post(id):
    publication = Post.query.get_or_404(id)
    return render_template('post.html',  publication=publication)


@app.route("/post/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.publication'))
