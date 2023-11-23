import os
import requests
from flask import Flask, render_template, redirect, request, session, g, flash, jsonify, abort
from models import db, connect_db, User, Pokemon
from functions import create_new_pokemon, count_unique_species
from forms import UserForm, UserLoginForm
from pokeapi import get_random_pokemon
from datetime import datetime


CURRENT_USER_KEY = "current_user"


def create_app(config_name='default'):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pokegacha-test'
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            os.environ.get('DATABASE_URL', 'postgresql:///pokegacha'))

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
        app.config['SECRET_KEY'] = os.environ.get(
            'SECRET_KEY', "it's a secret")

    app.app_context().push()
    connect_db(app)

    # if config_name != 'testing':
    #     db.create_all()
    # db.drop_all()
    # db.create_all()

    return app


app = create_app()


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

    return redirect('/login')


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
                session[CURRENT_USER_KEY] = user.id
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
    """displays user profile"""
    user = User.query.get_or_404(user_id)
    unique_species = count_unique_species(user.user_pokemons)
    total_rolls = user.total_rolls

    return render_template('profile.html', user=user, unique_species=unique_species, total_rolls=total_rolls)


@app.route('/pokeroll', methods=["GET", "POST"])
def handle_pokeroll():
    """Display Pokemon Roll Page"""
    if not g.user:
        return redirect('login')

    return render_template('pokeroll.html')


@app.route('/gacha')
def roll_random_pokemon():
    """Get a random pokemon and data from the Poke Api"""

    if not g.user:
        return redirect('login')
    try:
        pokemon_data = get_random_pokemon()
        if pokemon_data:
            g.user.total_rolls += 1
            db.session.commit()

            print(f'{g.user.username} has rolled {g.user.total_rolls} times')

            return jsonify(pokemon_data), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to retrieve Pokemon data'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to retrieve Pokemon data: {e}'}), 500


@app.route('/catch', methods=["POST"])
def catch_pokemon():
    """Process User Catch Pokemon and save to database"""
    if not g.user:
        return redirect('login')
    try:

        pokemon = request.get_json()
        new_pokemon = create_new_pokemon(pokemon, g.user)

        db.session.add(new_pokemon)
        db.session.commit()
        print(f'{new_pokemon.name} added to database')

        print(
            f'{new_pokemon.name} added to {g.user.username}\'s pokemon collection')

        return jsonify({"message": "Pokemon caught successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/collection')
def show_collection():
    """Show User's Pokemon Collection"""
    if not g.user:
        return redirect('login')

    pokemon_collection = User.query.get_or_404(g.user.id).user_pokemons

    return render_template('collection.html', pokemon=pokemon_collection, user=g.user)
