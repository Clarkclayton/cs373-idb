import sys
sys.path.append("..") # Adds higher directory to python modules path.

from flask import Flask, render_template
import Models
import json
from collections import OrderedDict

app = Flask(__name__)


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

with open("static/type/10.json") as fi:
    fire_data = json.load(fi)

with open("static/type/11.json") as fi:
    water_data = json.load(fi)

with open("static/type/12.json") as fi:
    grass_data = json.load(fi)

fireType = Models.Types(fire_data)
grassType = Models.Types(grass_data)
waterType = Models.Types(water_data)

fireType.resistance = [grassType]
fireType.strength = [grassType]
fireType.immunity = [grassType]

type_dict = { "10" : fireType, "11" : waterType, "12" : grassType}


with open("static/moves/1.json") as file:
    pound_data = json.load(file)
    pound_data["img"] = "static/img/fire_type.png"

with open("static/moves/2.json") as file:
    karatechop_data = json.load(file)
    karatechop_data["img"] = "static/img/fire_type.png"

with open("static/moves/3.json") as file:
    doubleslap_data = json.load(file)
    karatechop_data["img"] = "static/img/fire_type.png"

moves_dict = {"1": pound_data, "2": karatechop_data, "3": doubleslap_data}

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
    pk = pokemon_dict[pokemon_number]
    return render_template('pokemon.html',
            p_id=pk.ID,
            name=pk.name,
            p_type1=pk.pType1,
            p_type2=pk.pType2,
            stats=pk.baseStats)

@app.route('/move/<move_id>')
def move(move_id):
    move = moves_dict[move_id]

    return render_template('move.html',
            move_id=move.ID,
            move_accuracy=move.accuracy,
            move_pp=move.pp,
            move_priority=move.priority,
            move_power=move.power,
            move_class=move.dmg_class,
            move_type=move.m_type)

@app.route('/type/<type_id>')
def type(type_id):
    t = get_type(type_id)
    type_list = [type_dict["10"]]
    return render_template('type.html', ty=t, type_img='/static/img/fire_type.png', type_list=type_list)

if __name__ == '__main__':
    app.run(debug=True)
