from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User model."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default='/static/images/default-pic.png')
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def register(cls, username, password, email):
        """Register user with hashed password and return user."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        user = User(
            username=username,
            password=hashed_utf8,
            email=email
        )
        db.session.add(user)

        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            error_message = "Username taken, please choose another"
            return error_message
        except Exception as e:
            db.session.rollback()
            error_message = "An unexpected error occurred during registration."
            return error_message

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct."""

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Pokemon(db.Model):
    """Pokemon model."""

    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    obtained_at = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    species = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=True, default="Unknown")
    height = db.Column(db.Integer, nullable=True, default="Unknown")
    weight = db.Column(db.Integer, nullable=True, default="Unknown")
    image = db.Column(db.Text, nullable=True,
                      default="/static/images/default-pokemon.png")

    def __repr__(self):
        return f"<Pokemon #{self.id}: {self.name}, {self.species}, {self.type}>"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
