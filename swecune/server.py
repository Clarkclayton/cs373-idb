import sys
sys.path.append("..") # Adds higher directory to python modules path.

from flask import Flask, render_template
import Models
import json
from collections import OrderedDict

app = Flask(__name__)


with open("static/pokemon/1.json") as fi:
  bulba_data = json.load(fi)

pokemon_dict = {"1": Models.Pokemon(bulba_data)}

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

if __name__ == '__main__':
  app.run(debug=True)