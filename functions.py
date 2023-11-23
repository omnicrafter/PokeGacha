from models import Pokemon


def create_new_pokemon(pokemon, user):
    name = pokemon.get('species')
    if name:
        name = name.capitalize()
    species = pokemon.get('species')
    image = pokemon.get('image')
    image_shiny = pokemon.get('image_shiny')
    type1 = pokemon.get('type1')
    type2 = pokemon.get('type2')
    type3 = pokemon.get('type3')
    height = pokemon.get('height')
    weight = pokemon.get('weight')

    print(name, species, image, image_shiny,
          type1, type2, type3, height, weight)

    new_pokemon = Pokemon(
        name=name,
        species=species,
        image=image,
        image_shiny=image_shiny,
        type1=type1,
        type2=type2,
        type3=type3,
        height=height,
        weight=weight,
        owner_id=user.id
    )

    return new_pokemon


def count_unique_species(user_pokemons):
    """Count the number of unique species in the user's Pokemon collection."""
    unique_species_count = len(
        set(pokemon.species for pokemon in user_pokemons))
    return unique_species_count
