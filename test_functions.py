import unittest
from app import create_app, db, Pokemon, User, create_new_pokemon, count_unique_species


class PokemonFunctionTestCase(unittest.TestCase):
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

    def test_create_new_pokemon(self):
        user = User.register('testuser', 'password123', 'testuser@example.com')
        db.session.add(user)
        db.session.commit()

        pokemon_data = {
            'species': 'pikachu',
            'image': '/static/images/pikachu.png',
            'type1': 'Electric',
            'height': 40,
            'weight': 60
        }

        new_pokemon = create_new_pokemon(pokemon_data, user)
        db.session.add(new_pokemon)
        db.session.commit()

        self.assertIsInstance(new_pokemon, Pokemon)
        self.assertEqual(new_pokemon.name, 'Pikachu')
        self.assertEqual(new_pokemon.species, 'pikachu')
        self.assertEqual(new_pokemon.image, '/static/images/pikachu.png')
        self.assertEqual(new_pokemon.type1, 'Electric')
        self.assertEqual(new_pokemon.height, 40)
        self.assertEqual(new_pokemon.weight, 60)
        self.assertEqual(new_pokemon.owner_id, user.id)

    def test_count_unique_species(self):
        user = User.register('testuser', 'password123', 'testuser@example.com')
        db.session.add(user)
        db.session.commit()

        # Create some Pokemon for the user with different species
        species_list = ['Bulbasaur', 'Charmander', 'Squirtle', 'Bulbasaur']
        for species in species_list:
            new_pokemon = Pokemon(
                name=species, species=species, owner_id=user.id)
            db.session.add(new_pokemon)

        db.session.commit()

        user_pokemons = user.user_pokemons

        unique_species_count = count_unique_species(user_pokemons)
        self.assertEqual(unique_species_count, 3)
