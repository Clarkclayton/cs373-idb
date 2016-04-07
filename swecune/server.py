import itertools
import json
import sys

from flask import Flask, render_template, request
from sqlalchemy.orm import sessionmaker

sys.path.append("../.")

from models import *

app = Flask(__name__)
dialect = 'mysql+pymysql'
username = 'guestbook-user'
password = 'guestbook-user-password'
host = '104.130.22.72'
port = '3306'
database = 'guestbook'

engine = create_engine('{}://{}:{}@{}:{}/{}'.format(dialect, username, password, host, port, database)).connect()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, autocommit=True)


@app.route('/test')
def test():
    session = Session()
    x = session.query(Pokemon).filter(Pokemon.name == 'bulbasaur').all()
    print(x)
    return json.dumps([{'name': y.name, 'id': y.id,} for y in x])


@app.route('/test/1')
def test2():
    session = Session()
    x = session.query(Pokemon).filter(Pokemon.id == 1).one()
    print(x)
    return json.dumps({'name': x.name, 'id': x.id})


"""
Andrew's API Stuff here
"""


@app.route('/api/min_pokemon')
def api_min_pokemons():
    session = Session()
    pokemons_min_dictified = [pokemon.min_dictify() for pokemon in session.query(Pokemon).all()]
    return json.dumps(pokemons_min_dictified)


@app.route('/api/min_pokemon/<pokemon_id>')
def api_min_pokemon(pokemon_id):
    session = Session()
    pokemon_min_dictified = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first().min_dictify()
    return json.dumps(pokemon_min_dictified)


@app.route('/api/pokemon')
def api_pokemons():
    session = Session()
    offset = request.args.get('offset') if request.args.get('offset') != None else 0
    pokemon_per_page = request.args.get('limit') if request.args.get('limit') else 10

    pokemons_dictified = [pokemon.dictify() for pokemon in
                          session.query(Pokemon).limit(pokemon_per_page).offset(offset).all()]
    return json.dumps(pokemons_dictified)


@app.route('/api/pokemon/<pokemon_id>')
def api_pokemon(pokemon_id):
    session = Session()
    pokemon_dictified = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first().dictify()
    return json.dumps(pokemon_dictified)


@app.route('/api/move')
def api_moves():
    session = Session()
    offset = request.args.get('offset') if request.args.get('offset') != None else 0
    moves_per_page = request.args.get('limit') if request.args.get('limit') else 10

    moves_dictified = [move.dictify() for move in session.query(Move).limit(moves_per_page).offset(offset).all()]
    return json.dumps(moves_dictified)


@app.route('/api/move/<move_id>')
def api_move(move_id):
    session = Session()
    move_dictified = session.query(Move).filter(Move.id == move_id).first().dictify()
    return json.dumps(move_dictified)


@app.route('/api/type')
def api_types():
    session = Session()
    types_dictified = [type.dictify() for type in session.query(Type).all()]
    return json.dumps(types_dictified)


@app.route('/api/type/<type_id>')
def api_type(type_id):
    session = Session()
    type_dictified = session.query(Type).filter(Type.id == type_id).first().dictify()
    return json.dumps(type_dictified)


# def get_type(id):
#     type_dict = OrderedDict([
#         ("name", "Fire"),
#         ("numPrimary", 5),
#         ("numSecondary", 2),
#         ("Generation", 1),
#         ("numMoves", 123)
#     ])
#     return type_dict
#
#
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/pokemon/<pokemon_id>')
def pokemon(pokemon_id):
    session = Session()
    pk = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    if pk is None:
        return render_template('404.html')
    return render_template('pokemon.html', pk=pk)


# @app.route('/move/<move_id>')
# def move(move_id):
#     if move_id not in moves_dict:
#         return render_template('404.html')
#     move = moves_dict[move_id]
#     pk_learn_list = can_learn_move_dict[move_id]
#
#     return render_template('move.html',
#                            move_name=move.name,
#                            move_accuracy=move.accuracy,
#                            move_pp=move.pp,
#                            move_priority=move.priority,
#                            move_power=move.power,
#                            move_class=move.dmg_class,
#                            move_type=move.m_type,
#                            move_type_id=move.m_type_id,
#                            pk_learn_list=pk_learn_list)
#
#
@app.route('/type/<type_id>')
def type(type_id):
    session = Session()
    ty = session.query(Type).filter(Type.id == type_id).first()
    if ty is None:
        return render_template('404.html')
    print(ty.double_damage_to)

    relations_to=list(itertools.zip_longest(ty.double_damage_to, ty.half_damage_to, ty.no_damage_to))
    relations_from=list(itertools.zip_longest(ty.double_damage_from, ty.half_damage_from, ty.no_damage_from))
    return render_template('type.html', ty=ty, relations_to=relations_to, relations_from=relations_from)


@app.route('/pokemon')
def pokemon_all():
    return render_template('pokemon_all.html')


#
# @app.route('/type')
# def type_all():
#     return render_template('type_all.html', type_list=type_dict.values())
#
#
# @app.route('/move')
# def move_all():
#     return render_template('moves_all.html', moves=moves_dict.values())
#
#
@app.errorhandler(404)
def page_not_found(error):
    # app.logger.error('Page Not Found: %s', (request.path))
    return render_template('404.html'), 404


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
