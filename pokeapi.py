import requests
from random import randint

poke_species_url = 'https://pokeapi.co/api/v2/pokemon-species/'


def get_random_pokemon():
    def get_random_poke_id():
        """Return a random pokemon id out of 1292"""
        return randint(1, 1017)

    poke_url = 'https://pokeapi.co/api/v2/pokemon/'
    full_url = f'{poke_url}{get_random_poke_id()}'

    poke_response = requests.get(full_url)

    print(full_url)
    print(f"*************{poke_response}")

    try:
        pokemon_data = poke_response.json()

        name = pokemon_data["species"]["name"]
        species = pokemon_data["species"]["name"]
        type1 = pokemon_data["types"][0]["type"]["name"]
        type2 = "Unknown"
        if len(pokemon_data["types"]) > 1:
            type2 = pokemon_data["types"][1]["type"]["name"]
        type3 = "Unknown"
        if len(pokemon_data["types"]) > 2:
            type3 = pokemon_data["types"][2]["type"]["name"]

        height = pokemon_data["height"]
        weight = pokemon_data["weight"]
        image = pokemon_data["sprites"]["front_default"]
        image_shiny = "Unknown"
        if pokemon_data["sprites"]["front_shiny"]:
            image_shiny = pokemon_data["sprites"]["front_shiny"]

        pokemon = {
            "name": name,
            "species": species,
            "type1": type1,
            "type2": type2,
            "type3": type3,
            "height": height,
            "weight": weight,
            "image": image,
            "image_shiny": image_shiny
        }

        print(name, species, type1, type2, type3,
              height, weight, image, image_shiny)

        return pokemon

    except Exception as e:
        print(f"{e}")
