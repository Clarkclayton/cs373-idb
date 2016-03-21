import sys
sys.path.append("..") # Adds higher directory to python modules path.

from flask import Flask, render_template
import Models
import json
app = Flask(__name__)


with open("static/pokemon/1.json") as fi:
    bulba_data = json.load(fi)

pokemon_dict = {"1": Models.Pokemon(bulba_data)}

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

if __name__ == '__main__':
    app.run(debug=True)
