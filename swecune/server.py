import itertools
import json
import sys
from functools import wraps

from flask import Flask, render_template, request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from werkzeug.wrappers import Response

sys.path.append("../.")

from models import *

app = Flask(__name__)
dialect = 'mysql+pymysql'
username = 'guestbook-user'
password = 'guestbook-user-password'
host = '104.130.22.72'
port = '3306'
database = 'guestbook'

engine = create_engine('{}://{}:{}@{}:{}/{}'.format(dialect, username, password, host, port, database),
                       pool_recycle=3600).connect()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, autocommit=True)


class complicated_fucking_decorator(object):
    def __init__(self, calling_type, *extra_args):
        self.calling_type = calling_type
        self.extra_args = extra_args

    def __call__(self, func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
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
                except:
                    # It will reestablish the connection. So if the page is reloaded, the function the connection is new again
                    # TODO: How to resume?
                    raise exc.DisconnectionError()

        return func_wrapper


@app.route('/api/min_pokemon')
@complicated_fucking_decorator(True)
def api_min_pokemons(session):
    return [pokemon.min_dictify() for pokemon in session.query(Pokemon).all()]


@app.route('/api/min_pokemon/<pokemon_id>')
@complicated_fucking_decorator(True)
def api_min_pokemon(session, pokemon_id):
    resp = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    return resp.min_dictify() if resp else {}


@app.route('/api/pokemon')
@complicated_fucking_decorator(True)
def api_pokemons(session):
    offset = request.args.get('offset') if request.args.get('offset') is not None else 0
    pokemon_per_page = request.args.get('limit') if request.args.get('limit') else 10
    return [pokemon.dictify() for pokemon in session.query(Pokemon).limit(pokemon_per_page).offset(offset).all()]


@app.route('/api/pokemon/<pokemon_id>')
@complicated_fucking_decorator(True)
def api_pokemon(session, pokemon_id):
    resp = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    return resp.min_dictify() if resp else {}


@app.route('/api/move')
@complicated_fucking_decorator(True)
def api_moves(session):
    offset = request.args.get('offset') if request.args.get('offset') is not None else 0
    moves_per_page = request.args.get('limit') if request.args.get('limit') else 10
    return [move.dictify() for move in session.query(Move).limit(moves_per_page).offset(offset).all()]


@app.route('/api/move/<move_id>')
@complicated_fucking_decorator(True)
def api_move(session, move_id):
    resp = session.query(Move).filter(Move.id == move_id).first()
    return resp.dictify() if resp else {}


@app.route('/api/type')
@complicated_fucking_decorator(True)
def api_types(session):
    return [type.dictify() for type in session.query(Type).all()]


@app.route('/api/type/<type_id>')
@complicated_fucking_decorator(True)
def api_type(session, type_id):
    resp = session.query(Type).filter(Type.id == type_id).first()
    return resp.dictify() if resp else {}


@app.route('/pokemon/<pokemon_id>')
@complicated_fucking_decorator(False, 'pokemon.html')
def pokemon(session, pokemon_id):
    resp = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
    return {'pk': resp} if resp else None


@app.route('/move/<move_id>')
@complicated_fucking_decorator(False, 'move.html')
def move(session, move_id):
    resp = session.query(Move).filter(Move.id == move_id).first()
    return {'mv': resp} if resp else None


@app.route('/type/<type_id>')
@complicated_fucking_decorator(False, 'type.html')
def type(session, type_id):
    resp = session.query(Type).filter(Type.id == type_id).first()
    ret = {'ty': resp}
    if resp is not None:
        ret['relations_to'] = list(itertools.zip_longest(resp.double_damage_to, resp.half_damage_to, resp.no_damage_to))
        ret['relations_from'] = list(
            itertools.zip_longest(resp.double_damage_from, resp.half_damage_from, resp.no_damage_from))
    return ret if resp else None


@app.route('/pokemon')
def pokemon_all():
    return render_template('pokemon_all.html')


# @app.route('/type')
# def type_all():
#     return render_template('type_all.html', type_list=type_dict.values())
#
#
@app.route('/move')
def move_all():
    return render_template('moves_all.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
