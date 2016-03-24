import json
from collections import OrderedDict

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import Models

app = Flask(__name__)
db = SQLAlchemy(app)

with open("static/pokemon/1.json") as fi:
    bulba_data = json.load(fi)
with open("static/pokemon/4.json") as fi:
    char_data = json.load(fi)
with open("static/pokemon/7.json") as fi:
    squirt_data = json.load(fi)

bulbasaur = Models.Pokemon(bulba_data)
charmander = Models.Pokemon(char_data)
squirtle = Models.Pokemon(squirt_data)

pokemon_dict = {"1": bulbasaur, "4": charmander, "7": squirtle}

with open("static/type/10.json", 'r', encoding='cp866') as fi:
    fire_data = json.load(fi)

with open("static/type/11.json", 'r', encoding='cp866') as fi:
    water_data = json.load(fi)

with open("static/type/12.json", 'r', encoding='cp866') as fi:
    grass_data = json.load(fi)

fireType = Models.Types(fire_data)
grassType = Models.Types(grass_data)
waterType = Models.Types(water_data)

fireType.resistance = [grassType]
fireType.strength = [grassType]
fireType.immunity = [grassType]
fireType.resistance = [grassType]

waterType.resistance = [fireType]
waterType.strength = [fireType]
waterType.immunity = [waterType]

grassType.resistance = [grassType]
grassType.strength = [waterType]
grassType.immunity = [grassType]

type_dict = {"10": fireType, "11": waterType, "12": grassType}

with open("static/moves/33.json", 'r', encoding='cp866') as file:
    tackle_data = json.load(file)

with open("static/moves/43.json", 'r', encoding='cp866') as file:
    leer_data = json.load(file)

with open("static/moves/52.json", 'r', encoding='cp866') as file:
    ember_data = json.load(file)

tackleMove = Models.Moves(tackle_data)
leerMove = Models.Moves(leer_data)
emberMove = Models.Moves(ember_data)

moves_dict = {"33": tackleMove, "43": leerMove, "52": emberMove}
can_learn_move_dict = {"33": [squirtle, bulbasaur], "43": [charmander], "52": [charmander]}


def get_type(id):
    type_dict = OrderedDict([
        ("name", "Fire"),
        ("numPrimary", 5),
        ("numSecondary", 2),
        ("Generation", 1),
        ("numMoves", 123)
    ])
    return type_dict


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/pokemon/<pokemon_number>')
def pokemon(pokemon_number):
    if pokemon_number not in pokemon_dict:
        return render_template('404.html')
    pk = pokemon_dict[pokemon_number]
    return render_template('pokemon.html',
                           p_id=pk.ID,
                           name=pk.name,
                           p_type1=pk.pType1,
                           p_type2=pk.pType2,
                           p_type_id1=pk.pTypeId1,
                           p_type_id2=pk.pTypeId2,
                           stats=pk.baseStats,
                           moves=moves_dict.values())


@app.route('/move/<move_id>')
def move(move_id):
    if move_id not in moves_dict:
        return render_template('404.html')
    move = moves_dict[move_id]
    pk_learn_list = can_learn_move_dict[move_id]

    return render_template('move.html',
                           move_name=move.name,
                           move_accuracy=move.accuracy,
                           move_pp=move.pp,
                           move_priority=move.priority,
                           move_power=move.power,
                           move_class=move.dmg_class,
                           move_type=move.m_type,
                           move_type_id=move.m_type_id,
                           pk_learn_list=pk_learn_list)


@app.route('/type/<type_id>')
def type(type_id):
    if type_id not in type_dict:
        return render_template('404.html')
    t = type_dict[type_id]
    return render_template('type.html',
                           mv_list=moves_dict.values(),
                           ty=t,
                           superEffective=zip(t.strength, t.resistance, t.immunity),
                           numPrimary="134",
                           numSecondary="56",
                           numMoves="42",
                           type_img='/static/img/fire_type.png',
                           pokemon_list=pokemon_dict.values(),
                           pokemon_url='/static/img/pokemon1.png')


@app.route('/pokemon')
def pokemon_all():
    return render_template('pokemon_all.html', pokemon_list=pokemon_dict.values())


@app.route('/type')
def type_all():
    return render_template('type_all.html', type_list=type_dict.values())


@app.route('/move')
def move_all():
    return render_template('moves_all.html', moves=moves_dict.values())


@app.errorhandler(404)
def page_not_found(error):
    # app.logger.error('Page Not Found: %s', (request.path))
    return render_template('404.html'), 404


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
