from ourModels import Pokemon, Move, Type


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
        average_stats = sum(hp, attack, defense, special_attack, special_defense, speed) // 6
        primary_type = id_from_url(json['types'][0]['type']['url']) if len(json['types']) == 1 else id_from_url(
            json['types'][1]['type']['url'])
        secondary_type = id_from_url(json['types'][0]['type']['url']) if len(json['types']) == 2 else None
        moves = [id_from_url(move['url']) for move in json['moves']]
        return Pokemon(pokemon_id, name, hp, attack, defense, special_attack, special_defense, speed, average_stats,
                       primary_type, secondary_type, moves)

    @staticmethod
    def make_move_json(json):
        move_id = json['id']
        name = json['name']
        accuracy = json['accuracy']
        pp = json['pp']
        priority = json['priority']
        power = json['power']
        damage_class = json['damage_class']['name']
        move_type = id_from_url(json['type']['url'])
        return Move(move_id, name, accuracy, pp, priority, power, damage_class, move_type)

    @staticmethod
    def make_type_json(json):
        move_id = json['id']
        name = json['name']
        generation = id_from_url(json['generation']['url'])
        immunities = [id_from_url(p_type['url']) for p_type in json['no_damage_from']]
        strengths = [id_from_url(p_type['url']) for p_type in json['double_damage_to']]
        weaknesses = [id_from_url(p_type['url']) for p_type in json['double_damage_from']]
        return Type(id, name, generation, immunities, strengths, weaknesses)


def id_from_url(full_url):
    return full_url.split('/')[-2]
