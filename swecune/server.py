import itertools
import json
import subprocess
from functools import wraps

import requests
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.wrappers import Response

from models import Pokemon, Move, Type, Base

app = Flask(__name__)
dialect = 'mysql+pymysql'
username = 'guestbook-user'
password = 'guestbook-user-password'
host = '172.99.79.105'
port = '3306'
database = 'guestbook'

engine = create_engine('{}://{}:{}@{}:{}/{}'.format(dialect, username, password, host, port, database),
                       pool_recycle=3600).connect()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, autocommit=True)


class ComplicatedFuckingDecorator(object):
    def __init__(self, calling_type, *extra_args):
        self.calling_type = calling_type
        self.extra_args = extra_args

    def __call__(self, func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            global Session, engine
            while True:
                try:
                    session = Session()
                    ret = func(session, *args, **kwargs)
                    if self.calling_type:
                        resp = Response(json.dumps(ret), mimetype='application/json', status=200)
                    else:
                        if ret is None:
                            resp = render_template('404.html'), 404
                        else:
                            resp = render_template(*self.extra_args, **ret), 200
                    session.close()
                    return resp
                except Exception as e:
                    print(e)
                    engine = create_engine(
                        '{}://{}:{}@{}:{}/{}'.format(dialect, username, password, host, port, database),
                        pool_recycle=3600).connect()
                    Base.metadata.create_all(engine)
                    Session = sessionmaker(bind=engine, autocommit=True)

        return func_wrapper


@app.route('/api/run_tests')
def api_run_tests():
    try:
        test_results = subprocess.getoutput("python3 tests.py")
        return test_results
    except Exception as e:
        return str(e)


@app.route('/api/min_pokemon')
@ComplicatedFuckingDecorator(True)
def api_min_pokemons(session):
    return [pokemon.min_dictify() for pokemon in session.query(Pokemon).all()]


@app.route('/api/min_pokemon/<pokemon_id>')
@ComplicatedFuckingDecorator(True)
def api_min_pokemon(session, pokemon_id):
    resp = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    return resp.min_dictify() if resp else {}


@app.route('/api/pokemon')
@ComplicatedFuckingDecorator(True)
def api_pokemons(session):
    offset = request.args.get('offset') if request.args.get('offset') is not None else 0
    pokemon_per_page = request.args.get('limit') if request.args.get('limit') else 10
    return [pokemon.dictify() for pokemon in session.query(Pokemon).limit(pokemon_per_page).offset(offset).all()]


@app.route('/api/pokemon/<pokemon_id>')
@ComplicatedFuckingDecorator(True)
def api_pokemon(session, pokemon_id):
    resp = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    return resp.dictify() if resp else {}


@app.route('/api/min_move')
@ComplicatedFuckingDecorator(True)
def api_min_moves(session):
    return [move.min_dictify() for move in session.query(Move).filter(Move.type_id < 20).all()]


@app.route('/api/move')
@ComplicatedFuckingDecorator(True)
def api_moves(session):
    offset = request.args.get('offset') if request.args.get('offset') is not None else 0
    moves_per_page = request.args.get('limit') if request.args.get('limit') else 10
    return [move.dictify() for move in
            session.query(Move).filter(Move.type_id < 20).limit(moves_per_page).offset(offset).all()]


@app.route('/api/move/<move_id>')
@ComplicatedFuckingDecorator(True)
def api_move(session, move_id):
    resp = session.query(Move).filter(Move.id == move_id).first()
    return resp.dictify() if resp else {}


@app.route('/api/min_type')
@ComplicatedFuckingDecorator(True)
def api_min_types(session):
    return [type.min_dictify() for type in session.query(Type).filter(Type.id < 20).all()]


@app.route('/api/type')
@ComplicatedFuckingDecorator(True)
def api_types(session):
    return [type.dictify() for type in session.query(Type).filter(Type.id < 20).all()]


@app.route('/api/type/<type_id>')
@ComplicatedFuckingDecorator(True)
def api_type(session, type_id):
    resp = session.query(Type).filter(Type.id == type_id).first()
    return resp.dictify() if resp else {}


@app.route('/pokemon/<pokemon_id>')
@ComplicatedFuckingDecorator(False, 'pokemon.html')
def pokemon(session, pokemon_id):
    resp = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    return {'pk': resp} if resp else None


@app.route('/move/<move_id>')
@ComplicatedFuckingDecorator(False, 'move.html')
def move(session, move_id):
    resp = session.query(Move).filter(Move.id == move_id).first()
    test = {'mv': resp}
    return test if resp else None


@app.route('/type/<type_id>')
@ComplicatedFuckingDecorator(False, 'type.html')
def type(session, type_id):
    resp = session.query(Type).filter(Type.id == type_id).first()
    ret = {'ty': resp}
    if resp is not None:
        ret['relations_to'] = list(itertools.zip_longest(resp.double_damage_to, resp.half_damage_to, resp.no_damage_to))
        ret['relations_from'] = list(
            itertools.zip_longest(resp.double_damage_from, resp.half_damage_from, resp.no_damage_from))
    return ret if resp else None


@app.route('/search')
@ComplicatedFuckingDecorator(False, 'search_results.html')
def search(session):
    query = str(request.args.get('q', '')).split(' ')
    refined = [x for x in query if x != '']
    single_query = ' '.join(refined)

    return {
        'moves_all': session.query(Move).filter(
            Move.name.like('%' + str('%'.join(c for c in single_query)) + '%')).all(),
        'pokemon_all': session.query(Pokemon).filter(
            Pokemon.name.like('%' + str('%'.join(c for c in single_query)) + '%')).all(),
        'type_all': session.query(Type).filter(
            Type.name.like('%' + str('%'.join(c for c in single_query)) + '%')).all(),

        'pokemon': sum(
            [session.query(Pokemon).filter(Pokemon.name.like('%' + str('%'.join(c for c in q)) + '%')).all() for q in
             refined], []),
        'moves': sum(
            [session.query(Move).filter(Move.name.like('%' + str('%'.join(c for c in q)) + '%')).all() for q in
             refined], []),
        'type': sum(
            [session.query(Type).filter(Type.name.like('%' + str('%'.join(c for c in q)) + '%')).all() for q in
             refined], []),
        'search_terms': str(refined)
    }


@app.route('/pokemon')
def pokemon_all():
    return render_template('pokemon_all.html')


@app.route('/type')
def type_all():
    return render_template('type_all.html')


@app.route('/move')
def move_all():
    return render_template('moves_all.html')


@app.route('/games')
def games():
    return render_template('games.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template('404.html'), 404


@app.route('/ggmate')
def ggmate():
    poke_game_ids = [8339, 8340, 8341, 8342, 21341, 21343, 21344, 21345, 21346, 21347, 21348, 21349, 21350, 21351,
                     21352, 21353, 21354, 11081, 14742, 14745, 14747, 14754, 14758, 14759, 14761, 14762, 9191, 9201,
                     8330, 8334, 7553, 11099, 11102, 11103, 11105, 11106, 11107, 11109, 24364, 24379, 24382, 17166,
                     17167, 17169, 17170, 10018, 10023, 16532, 16535, 3827, 13137, 13138, 16589, 16597, 24464, 7235,
                     21339, 21340, 10141, 3318, 3322, 3325, 3326, 3328, 3329, 3332, 11770, 10068, 10069, 10070, 24325,
                     24328, 24331, 24348, 8328, 24413, 24425, 7709, 7713, 20675]
    ret = [requests.get('http://ggmate.me/api/game/' + str(id)).json() for id in poke_game_ids]
    return Response(json.dumps(ret), mimetype='application/json', status=200)


if __name__ == '__main__':
    app.run(debug=True)
