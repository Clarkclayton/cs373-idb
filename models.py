import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "swecune/"))

from swecune.server import db

pokemon_move = db.Table('pokemon_move',
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
                        db.Column('move_id', db.Integer, db.ForeignKey('move.id'))
                        )

type_1 = db.Table('type_1',
                  db.Column('id', db.Integer, primary_key=True),
                  db.Column('type_1', db.Integer, db.ForeignKey('type.id')),
                  db.Column('type_2', db.Integer, db.ForeignKey('type2.id'))
                  )

type_2 = db.Table('type_2',
                  db.Column('id', db.Integer, primary_key=True),
                  db.Column('type_1', db.Integer, db.ForeignKey('type.id')),
                  db.Column('type_2', db.Integer, db.ForeignKey('type2.id'))
                  )

type_3 = db.Table('type_3',
                  db.Column('id', db.Integer, primary_key=True),
                  db.Column('type_1', db.Integer, db.ForeignKey('type.id')),
                  db.Column('type_2', db.Integer, db.ForeignKey('type2.id'))
                  )

"""
Model for Pokemon.
This represents the metadata relating to a given Pokemon.
There exists a many to 1..2 relationship from Pokemon to Type.
There exists a many to many relationship from Pokemon to Move.
"""


class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    special_attack = db.Column(db.Integer)
    special_defense = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    average_stats = db.Column(db.Integer)

    primary_type = db.Column(db.Integer, db.ForeignKey('type.id'))
    secondary_type = db.Column(db.Integer, db.ForeignKey('type.id'))

    moves = db.relationship('Move', secondary=pokemon_move, backref=db.backref('pokemon', lazy='dynamic'))

    def __init__(self, id, name, hp, attack, defense, special_attack, special_defense, speed, average_stats,
                 primary_type, secondary_type, moves):
        self.id = id
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.average_stats = average_stats
        self.primary_type = primary_type
        self.secondary_type = secondary_type
        self.moves = moves

    @staticmethod
    def get_pokemon(id):
        return {
            "id": 1,
            "name" : "bulbasaur",
            "hp" : 1,
            "attack" : 1,
            "defense" : 1,
            "special_attack" : 1,
            "special_defense": 1,
            "speed" : 1,
            "average_stats" : 1,
            "primary_type" : 1,
            "secondary_type" : 2,
            "moves" : [1, 4, 2]
        }


"""
Model for Move.
This represents the metadata relating to a given Move that pokemon can have.
There exists a 1 to many relationship from Type to Move.
There exists a many to many relationship from Move to Pokemon.
"""


class Move(db.Model):
    __tablename__ = 'move'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    accuracy = db.Column(db.Integer)
    pp = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    power = db.Column(db.Integer)
    damage_class = db.Column(db.String(80), nullable=False)
    move_type = db.Column(db.Integer, db.ForeignKey('type.id'))

    def __init__(self, id, name, accuracy, pp, priority, power, damage_class, move_type):
        self.id = id
        self.name = name
        self.accuracy = accuracy
        self.pp = pp
        self.priority = priority
        self.power = power
        self.damage_class = damage_class
        self.move_type = move_type


"""
Model for Type.
This represents the metadata relating to a given Type that a Pokemon and Move can have.
There exists a many to many relationship from Type to Type.
There exists a 1..2 to many relationship from Type to Pokemon.
There exists a 1 to many relationship from Type to Move.
"""


class Type(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    generation = db.Column(db.Integer)

    moves = db.relationship('Move', backref='type', lazy='dynamic')
    pokemon = db.relationship('Pokemon', backref='type', lazy='dynamic')

    immunities = db.relationship('Type', secondary=type_1, backref=db.backref('type2', lazy='dynamic'))
    strengths = db.relationship('Type', secondary=type_1, backref=db.backref('type2', lazy='dynamic'))
    weaknesses = db.relationship('Type', secondary=type_1, backref=db.backref('type2', lazy='dynamic'))

    def __init__(self, id, name, generation, immunities, strengths, weaknesses):
        self.id = id
        self.name = name
        self.generation = generation
        self.immunities = immunities
        self.strengths = strengths
        self.weaknesses = weaknesses
