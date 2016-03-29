from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def splash():
    return 'Hello World!'


@app.route('/pokemon', methods=['GET'])
def all_pokemon():
    return 'all_pokemon'


@app.route('/pokemon/<pokemon_id>', methods=['GET'])
def one_pokemon(pokemon_id):
    return 'one_pokemon'


@app.route('/move', methods=['GET'])
def all_move():
    return 'all_move'


@app.route('/move/<move_id>', methods=['GET'])
def one_move(move_id):
    return 'one_move'


@app.route('/type', methods=['GET'])
def all_type():
    return 'all_type'


@app.route('/type/<type_id>', methods=['GET'])
def one_type(type_id):
    return 'one_type'


@app.route('/about', methods=['GET'])
def about():
    return 'about'


@app.errorhandler(404)
def page_not_found(error):
    return '404', 404


if __name__ == '__main__':
    app.run(debug=True)
