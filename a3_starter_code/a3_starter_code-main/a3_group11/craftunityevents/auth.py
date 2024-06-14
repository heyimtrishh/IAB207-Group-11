from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create a blueprint for authentication-related routes
authbp = Blueprint('auth', __name__)

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    # If the form is submitted and valid
    if register.validate_on_submit():
        # Get data from the form
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        contact_number = register.contact_number.data
        address = register.address.data
        # Check if the user already exists
        user = db.session.scalar(db.select(User).where(User.full_name == uname))
        if user:
            # User exists, flash a message and redirect to the register page
            flash('Username already exists, please try another')
            return redirect(url_for('auth.register'))
        # Hash the password
        pwd_hash = generate_password_hash(pwd)
        # Create a new User object
        new_user = User(full_name=uname, password_hash=pwd_hash, email_id=email, contact_number=contact_number, address=address)
        # Add the new user to the session and commit to the database
        db.session.add(new_user)
        db.session.commit()
        # Redirect to the main index page after successful registration
        return redirect(url_for('main.index'))
    else:
        # Render the registration template if the request is GET or the form is not valid
        return render_template('user.html', form=register, heading='Register')

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    # If the form is submitted and valid
    if login_form.validate_on_submit():
        # Get the username and password from the form
        user_name = login_form.user_name.data
        password = login_form.password.data
        # Query the user from the database
        user = db.session.scalar(db.select(User).where(User.full_name == user_name))
        # If user does not exist
        if user is None:
            error = 'Incorrect username, please try again.'  # Security risk to give this much info
        # If password does not match
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password, please try again.'
        if error is None:
            # If there are no errors, log in the user
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            # Flash the error message
            flash(error)
    # Render the login template
    return render_template('user.html', form=login_form, heading='Login')

@authbp.route('/logout')
@login_required
def logout():
    # Log out the user
    logout_user()
    # Redirect to the main index page
    return redirect(url_for('main.index'))
