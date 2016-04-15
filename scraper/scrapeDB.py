from sqlalchemy.orm import sessionmaker

from models import *

dialect = 'mysql+pymysql'
username = 'guestbook-user'
password = 'guestbook-user-password'
host = '172.99.79.105'
port = '3306'
database = 'guestbook'
engine = create_engine('{}://{}:{}@{}:{}/{}'.format(dialect, username, password, host, port, database)).connect()

Base = declarative_base()
Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

print('\nType')
result = engine.execute('SELECT * FROM type')
for row in result:
    print(row)

print('\nMove')
result = engine.execute('SELECT * FROM move')
for row in result:
    print(row)

print('\nPokemon')
result = engine.execute('SELECT * FROM pokemon')
for row in result:
    print(row)

print('\nDouble Damage From')
result = engine.execute('SELECT * FROM double_damage_from')
for row in result:
    print(row)

print('\nDouble Damage To')
result = engine.execute('SELECT * FROM double_damage_to')
for row in result:
    print(row)

print('\nHalf Damage From')
result = engine.execute('SELECT * FROM half_damage_from')
for row in result:
    print(row)

print('\nHalf Damage To')
result = engine.execute('SELECT * FROM half_damage_to')
for row in result:
    print(row)

print('\nNo Damage From')
result = engine.execute('SELECT * FROM no_damage_from')
for row in result:
    print(row)

print('\nNo Damage To')
result = engine.execute('SELECT * FROM no_damage_to')
for row in result:
    print(row)

# print('\nPokemon Move')
# result = engine.execute('SELECT count(*) FROM pokemon_move')
# for row in result:
#     print(row)
