from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from services.forms.forms import UpdateAccountForm
from .app import db, app
import os
import secrets
from PIL import Image

main = Blueprint('main', __name__)

publications = [
    {
        'user': 'pepe',
        'title': 'Publication 1',
        'description': 'First publication description',
        'priority': 'high',
        'status': 'active',
        'create_at': '2020-12-20'
    },
    {
        'user': 'pepe',
        'title': 'Publication 2',
        'description': 'Second publication description',
        'priority': 'medium',
        'status': 'active',
        'create_at': '2020-12-20'
    },
    {
        'user': 'pepe',
        'title': 'Publication 3',
        'description': 'Third publication description',
        'priority': 'low',
        'status': 'active',
        'create_at': '2020-12-20'
    }
]


@main.route('/publication')
def publication():
    return render_template('publication.html', publications=publications)


@main.route('/')
def index():
    return render_template('index.html')


def save_picture(form_picture):
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
        'static', filename='profile_pics/' + current_user.photo)
    return render_template('profile.html', name=current_user.email, photo=photo, form=form)


# @main.route('/publication')
# @login_required  # Must be log in to see publications.
# def publication():
#     return render_template('publication.html')
