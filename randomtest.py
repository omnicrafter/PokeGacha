import requests
from random import randint
from json import JSONDecodeError


def get_random_poke_id():
    """Return a random pokemon id out of 1292"""
    return randint(1, 1292)


poke_url = 'https://pokeapi.co/api/v2/pokemon/'
poke_species_url = 'https://pokeapi.co/api/v2/pokemon-species/'

poke_response = requests.get(f'{poke_url}{get_random_poke_id()}')

try:
    pokemon_data = poke_response.json()

    name = pokemon_data["species"]["name"]
    species = pokemon_data["species"]["name"]
    species_url = pokemon_data["species"]["url"]
    poke_type = pokemon_data["types"][0]["type"]["name"]
    poke_type2 = None
    if len(pokemon_data["types"]) > 1:
        poke_type2 = pokemon_data["types"][1]["type"]["name"]

    height = pokemon_data["height"]
    weight = pokemon_data["weight"]
    image = pokemon_data["sprites"]["front_default"]

    print(name, species, poke_type)
    if poke_type2 is not None:
        print(poke_type2)

except Exception as e:
    print(f"{e}")
