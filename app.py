import os
import requests
from flask import Flask, render_template, redirect, request, session, g, flash, abort
from models import db, connect_db, User, Pokemon
from forms import UserForm, UserLoginForm


CURRENT_USER_KEY = "current_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///pokegacha'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

app.app_context().push()
connect_db(app)
# db.create_all()


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURRENT_USER_KEY in session:
        g.user = User.query.get(session[CURRENT_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURRENT_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURRENT_USER_KEY in session:
        del session[CURRENT_USER_KEY]


@app.route('/')
def homepage():
    """Homepage Route"""

    return redirect('/signup')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle User Signup"""

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        existing_user = User.query.filter(User.username == username).first()
        if existing_user:
            flash("Username not available")
        else:
            result = User.register(username, password, email)

            if isinstance(result, User):
                user = result
                flash(
                    f"Welcome {user.username}! Your account has been successfully created.")
                return redirect(f'/users/{user.id}')
            else:
                flash(result)
                return redirect('/')

    if g.user:
        return redirect('/')

    return render_template("signup.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def handle_login():
    """Handle User Login"""

    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            do_login(user)
            flash(f'Welcome back, {user.username}')
            return redirect(f'/users/{user.id}')
        else:
            flash("Incorrect Credentials, Please try again.")
            return redirect('/login')

    if g.user:
        flash('You are already signed in')
        return redirect(f'/users/{g.user.id}')

    return render_template('login.html', form=form)


@app.route('/logout')
def handle_logout():
    """Handle User Logout"""

    if g.user:
        do_logout()
        flash('Log out successful')
        return redirect('/login')

    return redirect('/login')


@app.route('/users/<int:user_id>')
def display_user_profile(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('profile.html', user=user)


@app.route('/pokeroll')
def handle_pokeroll():
    if not g.user:
        return redirect('login')
