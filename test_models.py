import unittest
from datetime import datetime
from app import create_app, db, Pokemon, User


class PokemonModelTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app and configure it for testing
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create tables in the test database
        db.create_all()

    def tearDown(self):
        # Drop all tables after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user = User.register('testuser', 'password123', 'testuser@example.com')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.password.startswith('$2b$'))

    def test_create_user_duplicate_username(self):
        # Test handling of duplicate username during registration
        User.register('testuser', 'password123', 'testuser@example.com')
        duplicate_user = User.register(
            'testuser', 'anotherpassword', 'anotheruser@example.com')
        self.assertEqual(
            duplicate_user, "Username taken, please choose another")

    def test_create_user_duplicate_email(self):
        # Test handling of duplicate email during registration
        User.register('testuser', 'password123', 'testuser@example.com')
        duplicate_user = User.register(
            'anotheruser', 'anotherpassword', 'testuser@example.com')
        self.assertEqual(
            duplicate_user, "Username taken, please choose another")

    def test_authenticate_user(self):
        # Test user authentication
        User.register('testuser', 'password123', 'testuser@example.com')
        authenticated_user = User.authenticate('testuser', 'password123')
        self.assertIsInstance(authenticated_user, User)
        self.assertEqual(authenticated_user.username, 'testuser')

    def test_authenticate_user_invalid_password(self):
        # Test authentication with invalid password
        User.register('testuser', 'password123', 'testuser@example.com')
        authenticated_user = User.authenticate('testuser', 'wrongpassword')
        self.assertFalse(authenticated_user)

    def test_create_pokemon(self):
        user = User.register('testuser', 'password123', 'testuser@example.com')

        # Create a Pokemon instance associated with the user
        pokemon = Pokemon(
            name='Pikachu',
            species='Electric Mouse',
            type1='Electric',
            owner_id=user.id  # Associate the Pokemon with the user
        )

        # Add the Pokemon to the user's list of user_pokemons
        user.user_pokemons.append(pokemon)

        # Add the user and Pokemon to the session and commit
        db.session.add(user)
        db.session.commit()

        # Now the Pokemon should have an owner_id
        self.assertIsInstance(pokemon, Pokemon)
        self.assertEqual(pokemon.name, 'Pikachu')
        self.assertEqual(pokemon.species, 'Electric Mouse')
        self.assertEqual(pokemon.type1, 'Electric')
        self.assertEqual(pokemon.owner_id, user.id)

    def test_pokemon_representation(self):
        user = User.register('testuser', 'password123', 'testuser@example.com')
        pokemon = Pokemon(
            name='Bulbasaur',
            species='Seed Pokemon',
            type1='Grass',
            type2='Poison',
            owner_id=user.id
        )
        db.session.add(pokemon)
        db.session.commit()

        self.assertEqual(
            repr(pokemon), "<Pokemon #1: Bulbasaur, Seed Pokemon, Grass, Poison>")
