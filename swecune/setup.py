from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import username, password, host, port

SQLALCHEMY_DATABASE_URI_TEMP = '{engine}://{username}:{password}@{hostname}:{port}/'.format(
    engine='mysql+pymysql',
    username=username,
    password=password,
    hostname=host,
    port=port)

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_TEMP
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.engine.execute('CREATE DATABASE IF NOT EXISTS swecune;')
