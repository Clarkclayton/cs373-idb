import itertools
import json
import subprocess
from functools import wraps

from flask import Flask, render_template, request
from flask.ext.script import Manager
from werkzeug.wrappers import Response

import Scraping
from config import username, password, host, port, database
from models import db, Move, Type, Pokemon

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

manager = Manager(app)
db.init_app(app)

poke_game_ids = [8339, 8340, 8341, 8342, 21341, 21343, 21344, 21345, 21346, 21347, 21348, 21349, 21350, 21351,
                 21352, 21353, 21354, 11081, 14742, 14745, 14747, 14754, 14758, 14759, 14761, 14762, 9191, 9201,
                 8330, 8334, 7553, 11099, 11102, 11103, 11105, 11106, 11107, 11109, 24364, 24379, 24382, 17166,
                 17167, 17169, 17170, 10018, 10023, 16532, 16535, 3827, 13137, 13138, 16589, 16597, 24464, 7235,
                 21339, 21340, 10141, 3318, 3322, 3325, 3326, 3328, 3329, 3332, 11770, 10068, 10069, 10070, 24325,
                 24328, 24331, 24348, 8328, 24413, 24425, 7709, 7713, 20675]


class ComplicatedFuckingDecorator(object):
    def __init__(self, html_file):
        self.html_file = html_file

    def __call__(self, func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            if ret is None:
                return render_template('404.html'), 404
            else:
                return render_template(self.html_file, **ret), 200

        return func_wrapper


@app.route('/')
@ComplicatedFuckingDecorator('index.html')
def home():
    return {}


@app.route('/about')
@ComplicatedFuckingDecorator('about.html')
def about():
    return {}


@app.route('/pokemon')
@ComplicatedFuckingDecorator('pokemon_all.html')
def pokemon_all():
    return {}


@app.route('/type')
@ComplicatedFuckingDecorator('type_all.html')
def type_all():
    return {}


@app.route('/move')
@ComplicatedFuckingDecorator('moves_all.html')
def move_all():
    return {}


@app.route('/games')
@ComplicatedFuckingDecorator('games.html')
def games():
    return {}


@app.route('/search')
@ComplicatedFuckingDecorator('search_results.html')
def search():
    query = str(request.args.get('q', '')).split(' ')
    refined = [x for x in query if x != '']
    single_query = ' '.join(refined)

    return {
        'moves_all': Move.query.filter(Move.name.like('%' + str('%'.join(c for c in single_query)) + '%')).all(),
        'pokemon_all': Pokemon.query.filter(
            Pokemon.name.like('%' + str('%'.join(c for c in single_query)) + '%')).all(),
        'type_all': Type.query.filter(Type.name.like('%' + str('%'.join(c for c in single_query)) + '%')).all(),

        'pokemon': sum(
            [Pokemon.query.filter(Pokemon.name.like('%' + str('%'.join(c for c in q)) + '%')).all() for q in refined],
            []),
        'moves': sum(
            [Move.query.filter(Move.name.like('%' + str('%'.join(c for c in q)) + '%')).all() for q in refined], []),
        'type': sum([Type.query.filter(Type.name.like('%' + str('%'.join(c for c in q)) + '%')).all() for q in refined],
                    []),
        'search_terms': str(refined)
    }


@app.route('/type/<type_id>')
@ComplicatedFuckingDecorator('type.html')
def type(type_id):
    resp = Type.query.filter(Type.id == type_id).first()
    ret = {'ty': resp}
    if resp is not None:
        ret['relations_to'] = list(itertools.zip_longest(resp.double_damage_to, resp.half_damage_to, resp.no_damage_to))
        ret['relations_from'] = list(
            itertools.zip_longest(resp.double_damage_from, resp.half_damage_from, resp.no_damage_from))
    return ret if resp else None


@app.route('/pokemon/<pokemon_id>')
@ComplicatedFuckingDecorator('pokemon.html')
def pokemon(pokemon_id):
    resp = Pokemon.query.filter(Pokemon.id == pokemon_id).first()
    return {'pk': resp} if resp else None


@app.route('/move/<move_id>')
@ComplicatedFuckingDecorator('move.html')
def move(move_id):
    resp = Move.query.filter(Move.id == move_id).first()
    test = {'mv': resp}
    return test if resp else None


def ComplicatedJsonDecorator(func):
    @wraps(func)
    def thing(*args, **kwargs):
        return Response(json.dumps(func(*args, **kwargs)), mimetype='application/json', status=200)

    return thing


@app.route('/ggmate')
@ComplicatedJsonDecorator
def ggmate():
    jsons = []
    for id in poke_game_ids:
        with open('ggmate_json/game_' + str(id) + '.json', 'r') as outfile:
            jsons.append(json.load(outfile))
    return jsons


@app.route('/api/min_pokemon')
@ComplicatedJsonDecorator
def api_min_pokemons():
    return [pokemon.min_dictify() for pokemon in Pokemon.query.all()]


@app.route('/api/min_pokemon/<pokemon_id>')
@ComplicatedJsonDecorator
def api_min_pokemon(pokemon_id):
    resp = Pokemon.query.filter(Pokemon.id == pokemon_id).first()
    return resp.min_dictify() if resp else {}


@app.route('/api/pokemon')
@ComplicatedJsonDecorator
def api_pokemons():
    offset = request.args.get('offset') if request.args.get('offset') is not None else 0
    pokemon_per_page = request.args.get('limit') if request.args.get('limit') else 10
    return [pokemon.dictify() for pokemon in Pokemon.query.limit(pokemon_per_page).offset(offset).all()]


@app.route('/api/pokemon/<pokemon_id>')
@ComplicatedJsonDecorator
def api_pokemon(pokemon_id):
    resp = Pokemon.query.filter(Pokemon.id == pokemon_id).first()
    return resp.dictify() if resp else {}


@app.route('/api/min_move')
@ComplicatedJsonDecorator
def api_min_moves():
    return [move.min_dictify() for move in Move.query.filter(Move.type_id < 20).all()]


@app.route('/api/move')
@ComplicatedJsonDecorator
def api_moves():
    offset = request.args.get('offset') if request.args.get('offset') is not None else 0
    moves_per_page = request.args.get('limit') if request.args.get('limit') else 10
    return [move.dictify() for move in Move.query.filter(Move.type_id < 20).limit(moves_per_page).offset(offset).all()]


@app.route('/api/move/<move_id>')
@ComplicatedJsonDecorator
def api_move(move_id):
    resp = Move.query.filter(Move.id == move_id).first()
    return resp.dictify() if resp else {}


@app.route('/api/min_type')
@ComplicatedJsonDecorator
def api_min_types():
    return [type.min_dictify() for type in Type.query.filter(Type.id < 20).all()]


@app.route('/api/type')
@ComplicatedJsonDecorator
def api_types():
    return [type.dictify() for type in Type.query.filter(Type.id < 20).all()]


@app.route('/api/type/<type_id>')
@ComplicatedJsonDecorator
def api_type(type_id):
    resp = Type.query.filter(Type.id == type_id).first()
    return resp.dictify() if resp else {}


@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return render_template('404.html'), 404


@app.route('/api/run_tests')
def api_run_tests():
    try:
        test_results = subprocess.getoutput("python3 tests.py")
        return test_results
    except Exception as e:
        return str(e)


@manager.command
def create_db():
    print("create_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.create_all()


@manager.command
def test():
    print("test")
    app.config['SQLALCHEMY_ECHO'] = True
    result = db.engine.execute('show tables')
    for row in result:
        print(row)


@manager.command
def drop_db():
    print('dropping_tables')
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()


@manager.command
def scrape_db():
    Scraping.main(True)


if __name__ == "__main__":
    manager.run()
    # app.run()
