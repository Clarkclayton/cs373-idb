import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.Factory import Factory, pokemon, types, moves
from models import Base

# dialect = 'mysql+pymysql'
# username = 'root'
# password = '77corvette'
# host = '127.0.0.1'
# port = '3306'
# database = 'SWECUNEDB'

dialect = 'mysql+pymysql'
username = 'sthakkar14'
password = 'sthakkar14'
host = 'localhost'
port = '3306'
database = 'guestbook'

engine = create_engine('{}://{}:{}@{}:{}/{}'.format(dialect, username, password, host, port, database)).connect()

engine.execute('DROP TABLE IF EXISTS pokemon_move;')

engine.execute('DROP TABLE IF EXISTS double_damage_to;')
engine.execute('DROP TABLE IF EXISTS double_damage_from;')
engine.execute('DROP TABLE IF EXISTS half_damage_to;')

engine.execute('DROP TABLE IF EXISTS half_damage_from;')
engine.execute('DROP TABLE IF EXISTS no_damage_to;')
engine.execute('DROP TABLE IF EXISTS no_damage_from;')

engine.execute('DROP TABLE IF EXISTS pokemon;')
engine.execute('DROP TABLE IF EXISTS move;')
engine.execute('DROP TABLE IF EXISTS type;')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

endpoints = ['type', 'pokemon', 'move']
# endpoints = ['type']
base_url = "http://pokeapi.co/api/v2/"

for url_end in endpoints:
    resp = requests.get(base_url + url_end).json()

    urls = []
    while len(urls) != resp['count']:
        urls += [result['url'] for result in resp['results']]
        if resp['next'] is not None:
            resp = requests.get(resp['next']).json()

    x = getattr(Factory, 'make_' + url_end + '_json')
    for url in urls:
        print(url)
        x(requests.get(url).json())

Factory.add_relationships()

print('Add_all started')
session.add_all(value for value in types.values())
session.flush()
print('done')

print('Add_all started')
session.add_all(value for value in moves.values())
session.flush()
print('done')

print('Add_all started')
session.add_all(value for value in pokemon.values())
session.flush()
print('done')

session.close()

result = engine.execute('SELECT * FROM double_damage_to')
for row in result:
    print(row)

print('\n\n')

result = engine.execute('SELECT * FROM double_damage_from')
for row in result:
    print(row)

print('\n\n')
result = engine.execute('SELECT * FROM half_damage_to')
for row in result:
    print(row)

print('\n\n')
result = engine.execute('SELECT * FROM half_damage_from')
for row in result:
    print(row)

print('\n\n')
result = engine.execute('SELECT * FROM no_damage_to')
for row in result:
    print(row)

print('\n\n')
result = engine.execute('SELECT * FROM no_damage_from')
for row in result:
    print(row)

print('\n\n')
result = engine.execute('SELECT * FROM pokemon_move')
for row in result:
    print(row)

print('\n\n')
result = engine.execute('SELECT * FROM type')
for row in result:
    print(row)

print('\n\n')
result = engine.execute('SELECT * FROM move')
for row in result:
    print(row)

print('\n\n')
result = engine.execute('SELECT * FROM pokemon')
for row in result:
    print(row)

engine.close()
