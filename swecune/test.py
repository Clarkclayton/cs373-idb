import logging

from flask import Flask
from flask.ext.script import Manager

from config import username, password, host, port, database
from models import db

logging.basicConfig(level=logging.DEBUG)
logging.debug('Starting to log')

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


@app.route('/')
def base():
    return 'Hello World!'


@manager.command
def create_db():
    logging.debug("create_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.create_all()


@manager.command
def test():
    logging.debug("test")
    app.config['SQLALCHEMY_ECHO'] = True
    result = db.engine.execute('show tables')
    for row in result:
        print(row)


@manager.command
def drop_db():
    logging.debug('dropping_tables')
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()


@manager.command
def scrape_db():
    logging.debug('scrape_db')

    endpoints = ['type', 'pokemon', 'move']
    base_url = "http://pokeapi.co/api/v2/"


if __name__ == "__main__":
    manager.run()
