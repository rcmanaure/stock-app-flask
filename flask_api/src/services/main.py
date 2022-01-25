from fileinput import filename
from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

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


@main.route('/profile')
# @login_required  # Must be log in to see main page.
def profile():
    photo = url_for(
        'static', filename='profile_pics/' + current_user.photo)
    return render_template('profile.html', name=current_user.email, photo=photo)


# @main.route('/publication')
# @login_required  # Must be log in to see publications.
# def publication():
#     return render_template('publication.html')
