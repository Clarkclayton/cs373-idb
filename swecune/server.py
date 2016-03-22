import sys
sys.path.append("..") # Adds higher directory to python modules path.

from flask import Flask, render_template
import Models
import json

app = Flask(__name__)


with open("static/pokemon/1.json") as fi:
  bulba_data = json.load(fi)

bulbasaur = Models.Pokemon(bulba_data)
bulbasaur.pType1 = "grass"
bulbasaur.pType2 = "poison"

pokemon_dict = {"1": bulbasaur}

def get_move(id):
  return {
    "id": 1,
    "name": "Tackle",
    "accuracy": 100,
    "pp": 35,
    "priority": 0,
    "power" : 50,
    "is_special": False,
    "type": 0,
  }

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
  return render_template('move.html', move=move, type_img='/static/img/fire_type.png')

if __name__ == '__main__':
  app.run(debug=True)
