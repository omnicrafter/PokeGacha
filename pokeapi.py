import requests
from random import randint
import json

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
        
        


def json_serialize(data):
    """Serialize Python object to JSON-formatted string"""
    try:
        json_string = json.dumps(data, indent=2)

        return json_string

    except Exception as e:
        # Handle any potential exceptions during the serialization process
        print(f"Error during JSON serialization: {e}")
        return None


# data = get_random_pokemon()
# print(json_serialize(data))


# def get_all_pokemon():
#     poke_url = 'https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0'

#     poke_response = requests.get(poke_url)

#     pokemon_data = poke_response.json()

#     pokemon_seed_data = []

#     for pokemon in pokemon_data["results"]:
#         name = pokemon["name"]
#         url = pokemon["url"]
#         species = name

#         poke_request = requests.get(url)
#         pokemon_data = poke_request.json()

#         if pokemon_data["types"] != 0:
#             type1 = pokemon_data["types"][0]["type"]["name"]
#             type2 = None
#             if len(pokemon_data["types"]) > 1:
#                 type2 = pokemon_data["types"][1]["type"]["name"]
#             type3 = None
#             if len(pokemon_data["types"]) > 2:
#                 type3 = pokemon_data["types"][2]["type"]["name"]
#         if pokemon_data["height"]:
#             height = pokemon_data["height"]
#         if pokemon_data["weight"]:
#             weight = pokemon_data["weight"]
#         if pokemon_data["sprites"]["front_default"]:
#             image = pokemon_data["sprites"]["front_default"]
#         if pokemon_data["sprites"]["front_shiny"]:
#             image_shiny = pokemon_data["sprites"]["front_shiny"]

#         pokedata = {"name": name}

#         if species is not None:
#             pokedata["species"] = species
#         if type1 is not None:
#             pokedata["type1"]: type1
#         if type2 is not None:
#             pokedata["type2"]: type2
#         if type3 is not None:
#             pokedata["type3"]: type3
#         if height is not None:
#             pokedata["height"] = height
#         if weight is not None:
#             pokedata["weight"] = weight
#         if image is not None:
#             pokedata["image"] = image
#         if image_shiny is not None:
#             pokedata["image_shiny"] = image_shiny

#         pokemon_seed_data.append(pokedata)

#     return pokemon_seed_data
