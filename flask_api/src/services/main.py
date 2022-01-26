from flask import (Blueprint, render_template, url_for,
                   flash, redirect, request, abort)
from flask_login import login_required, current_user
from services.forms.forms import UpdateAccountForm, PostForm
from .app import User, db, app, Post
import os
import secrets
from PIL import Image
from flasgger import swag_from

# Init the Blueprints of be used in the mains routes.
main = Blueprint('main', __name__)


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


@main.route("/profile/delete", methods=['POST', 'GET'])
# To delete current logged User.
@login_required  # Must be log in.
def delete_profile():
    user = User.query.filter_by().first()
    if user.id != current_user.id:
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('main.publication'))


@main.route('/profile', methods=['GET'])
# Show the publications in the home page.
@swag_from('./docs/profile/profile_user.yaml')
def profile_user():
    form = UpdateAccountForm()
    return render_template('profile.html', form=form)


@main.route('/profile', methods=['POST'])
# To update the user account.
@login_required  # Must be log in.
@swag_from('./docs/profile/profile.yaml')
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
    return render_template('profile.html',
                           name=current_user.email,
                           photo=photo, form=form
                           )


@main.route('/', methods=['GET'])
# Show the publications in the home page.
@swag_from('./docs/publications/posts.yaml')
def publication():
    publications = Post.query.all()
    return render_template('publication.html', publications=publications)


@main.route("/post/new", methods=['POST'])
# To add a new Publication.
@login_required
@swag_from('./docs/publications/post.yaml')
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    user_id=current_user.id,
                    author=current_user.username
                    )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.publication'))
    return render_template('create_post.html',
                           form=form,
                           legend='New Publication'
                           )


@main.route("/post/<int:id>")
# To get a specific Publication.
def post(id):
    publication = Post.query.get_or_404(id)
    return render_template('post.html',  publication=publication)


@main.route("/post/<int:id>/update", methods=['GET', 'POST'])
# To update a specific Publication.
@login_required
@swag_from('./docs/publications/update_post.yaml')
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
        return redirect(url_for('main.post', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                           form=form, legend='Update Post')


@main.route("/post/<int:post_id>/delete", methods=['POST'])
# To delete a specific Publication.
@login_required
@swag_from('./docs/publications/delete_post.yaml')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.publication'))
