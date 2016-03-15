base_url = "http://pokeapi.co/api/v2"


def id_from_route(route):
    return route.split("/")[-2]


def make_pokemon(pd):
    pk = {}  # TODO: switch to a class
    pk["id"] = pd["id"]
    pk["name"] = pd["name"]

    types = [id_from_route(t["type"]["url"]) for t in pd["types"]]

    pk["type_1"] = types[0]
    pk["type_2"] = types[1] if len(types) > 1 else None

    pk["held_items"] = []  # TODO: make this work

    encounters = [id_from_route(t["location_area"]["url"]) for t in pd["location_area_encounters"]]
    pk["encounters"] = encounters

    moves = [id_from_route(t["move"]["url"]) for t in pd["moves"]]
    pk["moves"] = moves

    pk["sprite_id"] = None  # TODO: figure out how to handle this

    pk["base_stats"] = None  # TODO: what even are stats?

    pk["evolves_into"] = None  # TODO: traverse the ducking evolution tree

    return pk
