import sys
sys.path.append("..") # Adds higher directory to python modules path.

from flask import Flask, render_template
import Models
import json
from collections import OrderedDict

app = Flask(__name__)


with open("static/pokemon/1.json") as fi:
  bulba_data = json.load(fi)

bulbasaur = Models.Pokemon(bulba_data)
bulbasaur.pType1 = "grass"
bulbasaur.pType2 = "poison"

pokemon_dict = {"1": bulbasaur}

def get_move(id):
  move_dict = OrderedDict([
    ("ID", 1),
    ("Name", "Tackle"),
    ("Accuracy", 100),
    ("PP", 35),
    ("Priority", 0),
    ("Power", 50),
    ("Is Special", False),
    ("Type", 0)
  ])
  return move_dict

def get_type(id):
  type_dict = OrderedDict([
    ("name", "Fire"),
    ("numPrimary", 5),
    ("numSecondary", 2),
    ("Generation", 1),
    ("numMoves", 123)
  ])
  return type_dict
@app.route('/pokemon/<pokemon_number>')
def pokemon(pokemon_number):
  pk = pokemon_dict[pokemon_number]
  return render_template('pokemon.html',
                          p_id=pk.ID,
                          name=pk.name,
                          p_type1=pk.pType1,
                          p_type2=pk.pType2,
                          stats=pk.baseStats)

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/move/<move_id>')
def move(move_id):
  move = get_move(move_id)
  pk_list = [pokemon_dict["1"]]

  return render_template('move.html', move=move, type_img='/static/img/fire_type.png', pokemon_list=pk_list, pokemon_url='/static/img/pokemon1.png')

@app.route('/type/<type_id>')
def type(type_id):
  t = get_type(type_id)
  return render_template('type.html', ty=t, type_img='/static/img/fire_type.png')

if __name__ == '__main__':
  app.run(debug=True)
