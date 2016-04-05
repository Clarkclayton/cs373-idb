from db.models import Pokemon, Move, Type

pokemon_move_rel = {}
pokemon_primary_type_rel = {}
pokemon_secondary_type_rel = {}
type_move_rel = {}

double_damage_to_rel = {}
double_damage_from_rel = {}
half_damage_to_rel = {}
half_damage_from_rel = {}
no_damage_to_rel = {}
no_damage_from_rel = {}

pokemon = {}
moves = {}
types = {}


class Factory(object):
    @staticmethod
    def make_pokemon_json(json):
        pokemon_id = json['id']
        name = json['name']
        hp = json['stats'][5]['base_stat']
        attack = json['stats'][4]['base_stat']
        defense = json['stats'][3]['base_stat']
        special_attack = json['stats'][2]['base_stat']
        special_defense = json['stats'][1]['base_stat']
        speed = json['stats'][0]['base_stat']
        average_stats = sum([hp, attack, defense, special_attack, special_defense, speed]) // 6

        pokemon_primary_type_rel[pokemon_id] = id_from_url(json['types'][0]['type']['url']) if len(
            json['types']) == 1 else id_from_url(
            json['types'][1]['type']['url'])
        if len(json['types']) == 2:
            pokemon_secondary_type_rel[pokemon_id] = id_from_url(json['types'][0]['type']['url'])
        pokemon_move_rel[pokemon_id] = [id_from_url(move['move']['url']) for move in json['moves']]

        pokemon[pokemon_id] = Pokemon(id=pokemon_id,
                                      name=name,
                                      hp=hp,
                                      attack=attack,
                                      defense=defense,
                                      special_attack=special_attack,
                                      special_defense=special_defense,
                                      speed=speed,
                                      average_stats=average_stats)

    @staticmethod
    def make_move_json(json):
        move_id = json['id']
        name = json['name']
        accuracy = json['accuracy']
        pp = json['pp']
        priority = json['priority']
        power = json['power']
        damage_class = json['damage_class']['name']

        type_move_rel[move_id] = id_from_url(json['type']['url'])

        moves[move_id] = Move(id=move_id,
                              name=name,
                              accuracy=accuracy,
                              pp=pp,
                              priority=priority,
                              power=power,
                              damage_class=damage_class)

    @staticmethod
    def make_type_json(json):
        type_id = json['id']
        name = json['name']
        generation = id_from_url(json['generation']['url'])

        double_damage_to_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                         json['damage_relations']['double_damage_to']]
        double_damage_from_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                           json['damage_relations']['double_damage_from']]
        half_damage_to_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                       json['damage_relations']['half_damage_to']]
        half_damage_from_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                         json['damage_relations']['half_damage_from']]
        no_damage_to_rel[type_id] = [id_from_url(p_type['url']) for p_type in json['damage_relations']['no_damage_to']]
        no_damage_from_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                       json['damage_relations']['no_damage_from']]

        types[type_id] = Type(
            id=type_id,
            name=name,
            generation=generation
        )

    @staticmethod
    def add_relationships():
        for key, value in pokemon_move_rel.items():
            for x in value:
                pokemon[key].moves.append(moves[x])

        for key, value in pokemon_primary_type_rel.items():
            pokemon[key].primary_type = types[value]

        for key, value in pokemon_secondary_type_rel.items():
            pokemon[key].secondary_type = types[value]

        for key, value in type_move_rel.items():
            moves[key].type = types[value]

        for key, value in double_damage_to_rel.items():
            for x in value:
                types[key].double_damage_to.append(types[x])

        for key, value in double_damage_from_rel.items():
            for x in value:
                types[key].double_damage_from.append(types[x])

        for key, value in half_damage_to_rel.items():
            for x in value:
                types[key].half_damage_to.append(types[x])

        for key, value in half_damage_from_rel.items():
            for x in value:
                types[key].half_damage_from.append(types[x])

        for key, value in no_damage_to_rel.items():
            for x in value:
                types[key].no_damage_to.append(types[x])

        for key, value in no_damage_from_rel.items():
            for x in value:
                types[key].no_damage_from.append(types[x])


def id_from_url(full_url):
    return int(full_url.split('/')[-2])
