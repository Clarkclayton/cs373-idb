import json
import sys

import requests
from flask import Flask

from config import username, password, host, port, database
from models import Pokemon, Move, Type
from models import db

endpoints = ['type', 'pokemon', 'move']
base_url = "http://pokeapi.co/api/v2/"

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


def make_type_json(input_json):
    type_id = input_json['id']
    name = input_json['name']
    generation = id_from_url(input_json['generation']['url'])

    double_damage_to_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                     input_json['damage_relations']['double_damage_to']]
    double_damage_from_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                       input_json['damage_relations']['double_damage_from']]
    half_damage_to_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                   input_json['damage_relations']['half_damage_to']]
    half_damage_from_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                     input_json['damage_relations']['half_damage_from']]
    no_damage_to_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                 input_json['damage_relations']['no_damage_to']]
    no_damage_from_rel[type_id] = [id_from_url(p_type['url']) for p_type in
                                   input_json['damage_relations']['no_damage_from']]

    types[type_id] = Type(
        id=type_id,
        name=name,
        generation=generation
    )


def make_pokemon_json(input_json):
    pokemon_id = input_json['id']
    name = input_json['name']

    speed = input_json['stats'][0]['base_stat']
    special_defense = input_json['stats'][1]['base_stat']
    special_attack = input_json['stats'][2]['base_stat']
    defense = input_json['stats'][3]['base_stat']
    attack = input_json['stats'][4]['base_stat']
    hp = input_json['stats'][5]['base_stat']
    average_stats = sum([hp, attack, defense, special_attack, special_defense, speed]) // 6

    pokemon_primary_type_rel[pokemon_id] = id_from_url(input_json['types'][0]['type']['url']) if len(
        input_json['types']) == 1 else id_from_url(input_json['types'][1]['type']['url'])
    if len(input_json['types']) == 2:
        pokemon_secondary_type_rel[pokemon_id] = id_from_url(input_json['types'][0]['type']['url'])
    pokemon_move_rel[pokemon_id] = [id_from_url(move['move']['url']) for move in input_json['moves']]

    pokemon[pokemon_id] = Pokemon(id=pokemon_id,
                                  name=name,
                                  hp=hp,
                                  attack=attack,
                                  defense=defense,
                                  special_attack=special_attack,
                                  special_defense=special_defense,
                                  speed=speed,
                                  average_stats=average_stats)


def make_move_json(input_json):
    move_id = input_json['id']
    name = input_json['name']
    accuracy = input_json['accuracy']
    pp = input_json['pp']
    priority = input_json['priority']
    power = input_json['power']
    damage_class = input_json['damage_class']['name']

    type_move_rel[move_id] = id_from_url(input_json['type']['url'])

    moves[move_id] = Move(id=move_id,
                          name=name,
                          accuracy=accuracy,
                          pp=pp,
                          priority=priority,
                          power=power,
                          damage_class=damage_class)


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


def main(from_file):
    SQLALCHEMY_DATABASE_URI_TEMP = '{engine}://{username}:{password}@{hostname}:{port}/{database}'.format(
        engine='mysql+pymysql',
        username=username,
        password=password,
        hostname=host,
        port=port,
        database=database)

    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_TEMP
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    print('starting_scrape')
    for url_endpoint in endpoints:
        resp = requests.get(base_url + url_endpoint + '/?limit=100000').json()
        endpoint_class = globals()['make_' + url_endpoint + '_json']
        for result in resp['results']:
            url = result['url']
            print(url)
            try:
                if from_file:
                    with open('json_data/' + url_endpoint + '_' + url.split('/')[-2] + '.json') as data_file:
                        thing = json.load(data_file)
                else:
                    thing = requests.get(url).json()
                endpoint_class(thing)
            except Exception as e:
                print(e)
                print('Error at URL: ' + url)
    add_relationships()

    with app.app_context():
        print('starting inserts')
        db.drop_all()
        db.create_all()
        print('tables recreated')

        print('Add_all types started')
        for value in types.values():
            db.session.add(value)
        db.session.commit()
        print('done')

        print('Add_all moves started')
        for value in moves.values():
            db.session.add(value)
        db.session.commit()
        print('done')

        print('Add_all pokemon started')
        for value in pokemon.values():
            db.session.add(value)
        db.session.commit()
        print('done')


if __name__ == '__main__':
    main(sys.argv[1] == 'true')
    # main(True)
