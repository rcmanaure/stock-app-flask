from flask import Blueprint, render_template, redirect, url_for, request, flash
from services.forms.forms import RegistrationForm, LoginForm
from .app import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flasgger import swag_from
# Init the Blueprints of be used in the authorization routes.
auth = Blueprint('auth', __name__)


@auth.route('/login')
# Show Page to fill the credentials to Log In.
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@auth.route('/login', methods=['POST'])
@swag_from('./docs/auth/login.yaml')
# Logic to POST the credentials and Login.
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Find User in Database by Email.
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists then hash the password,
    #  and compare it to the hashed  password in the database.
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # If the remember button is True, save the credentials.
    login_user(user, remember=remember)

    # if the above check passes, redirect to the main page.
    return redirect(url_for('main.profile'))


@auth.route('/signup')
# Show the Registration Page.
def signup():
    form = RegistrationForm()
    return render_template('signup.html', form=form)


@auth.route('/signup', methods=['POST'])
@swag_from('./docs/auth/register.yaml')
# Logic to add an user.
def signup_post():
    form = RegistrationForm()
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')

    # check if the fields are empty.
    if not email and not password:
        flash('Please check requirements and try again.')
        return render_template('signup.html', form=form)
    else:
        # Check if the user exist in Database.
        user = User.query.filter_by(email=email).first()

        if user:
            # if user exist, we want to redirect back to signup page.
            flash('Email address already exists')
            return redirect(url_for('auth.signup'), form=form)

        # create a new user with the form data. Hash the password.
        new_user = User(email=email, username=name,
                        password=generate_password_hash(password,
                                                        method='sha256'))

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page.
        flash('Account created, Please Log In')
        return redirect(url_for('auth.login'))


@auth.route('/logout')
# To log out.
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.publication'))
