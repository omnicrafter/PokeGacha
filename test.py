import unittest
from datetime import datetime
from app import create_app, db, Pokemon, User, UserPokemon


class PokemonModelTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app and configure it for testing
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create tables in the test database
        db.create_all()

    def tearDown(self):
        # Remove tables from the test database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_pokemon_creation(self):
        # Create a Pokemon instance and add it to the database
        pokemon = Pokemon(
            name="TestPokemon",
            obtained_at=datetime.utcnow(),
            species="TestSpecies",
            type1="TestType",
            height=50,
            weight=100,
            image="/static/images/test-pokemon.png",
            image_shiny="/static/images/test-pokemon-shiny.png"
        )
        db.session.add(pokemon)
        db.session.commit()

        # Retrieve the Pokemon from the database
        retrieved_pokemon = Pokemon.query.filter_by(name="TestPokemon").first()

        # Assert that the retrieved Pokemon matches the created Pokemon
        self.assertEqual(retrieved_pokemon.name, "TestPokemon")
        self.assertEqual(retrieved_pokemon.species, "TestSpecies")
        self.assertEqual(retrieved_pokemon.type1, "TestType")
        self.assertEqual(retrieved_pokemon.height, 50)
        self.assertEqual(retrieved_pokemon.weight, 100)

    def test_default_values(self):
        # Create a Pokemon instance without specifying optional values
        pokemon = Pokemon(
            name="TestPokemon",
            obtained_at=datetime.utcnow(),
            species="TestSpecies"
        )
        db.session.add(pokemon)
        db.session.commit()

        # Retrieve the Pokemon from the database
        retrieved_pokemon = Pokemon.query.filter_by(name="TestPokemon").first()

        # Assert that the default values are set correctly
        self.assertEqual(retrieved_pokemon.type1, "Unknown")
        self.assertEqual(retrieved_pokemon.type2, "Unknown")
        self.assertEqual(retrieved_pokemon.type3, "Unknown")
        self.assertEqual(retrieved_pokemon.height, 0)
        self.assertEqual(retrieved_pokemon.weight, 0)


class UserPokemonModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()

    def test_user_pokemon_relationship(self):
        """Test the UserPokemon model relationships."""
        # Create a user
        user = User(username='testuser', password='password',
                    email='test@example.com')
        db.session.add(user)
        db.session.commit()

        # Create a Pokemon
        pokemon = Pokemon(name='Pikachu', species='Electric')
        db.session.add(pokemon)
        db.session.commit()

        # Create a UserPokemon relationship
        user_pokemon = UserPokemon(
            user_id=user.id, pokemon_id=pokemon.id, obtained_at=datetime.utcnow())
        db.session.add(user_pokemon)
        db.session.commit()

        # Retrieve the UserPokemon relationship from the database
        retrieved_relationship = UserPokemon.query.first()

        # Check if the relationship is correctly set up
        self.assertEqual(retrieved_relationship.user, user)
        self.assertEqual(retrieved_relationship.pokemon, pokemon)

    def test_user_pokemon_delete_orphan(self):
        """Test the delete-orphan cascade in the UserPokemon model."""
        # Create a user
        user = User(username='testuser', password='password',
                    email='test@example.com')
        db.session.add(user)
        db.session.commit()

        # Create a Pokemon
        pokemon = Pokemon(name='Bulbasaur', species='Grass')
        db.session.add(pokemon)
        db.session.commit()

        # Create a UserPokemon relationship
        user_pokemon = UserPokemon(
            user_id=user.id, pokemon_id=pokemon.id, obtained_at=datetime.utcnow())
        db.session.add(user_pokemon)
        db.session.commit()

        # Delete the user, which should also delete the associated UserPokemon
        db.session.delete(user)
        db.session.commit()

        # Check if the UserPokemon relationship is deleted
        retrieved_relationship = UserPokemon.query.first()
        self.assertIsNone(retrieved_relationship)


if __name__ == "__main__":
    unittest.main()
