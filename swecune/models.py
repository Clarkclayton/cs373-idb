from collections import OrderedDict

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

pokemon_move = db.Table('pokemon_move',
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
                        db.Column('move_id', db.Integer, db.ForeignKey('move.id')),
                        db.UniqueConstraint('pokemon_id', 'move_id', name='pokemon_move_relationship')
                        )

double_damage_to = db.Table('double_damage_to',
                            db.Column('id', db.Integer, primary_key=True),
                            db.Column('origin', db.Integer, db.ForeignKey('type.id')),
                            db.Column('opposing', db.Integer, db.ForeignKey('type.id')),
                            db.UniqueConstraint('origin', 'opposing', name='double_to_relation')
                            )

double_damage_from = db.Table('double_damage_from',
                              db.Column('id', db.Integer, primary_key=True),
                              db.Column('origin', db.Integer, db.ForeignKey('type.id')),
                              db.Column('opposing', db.Integer, db.ForeignKey('type.id')),
                              db.UniqueConstraint('origin', 'opposing', name='double_from_relation')
                              )

half_damage_to = db.Table('half_damage_to',
                          db.Column('id', db.Integer, primary_key=True),
                          db.Column('origin', db.Integer, db.ForeignKey('type.id')),
                          db.Column('opposing', db.Integer, db.ForeignKey('type.id')),
                          db.UniqueConstraint('origin', 'opposing', name='half_to_relation')
                          )

half_damage_from = db.Table('half_damage_from',
                            db.Column('id', db.Integer, primary_key=True),
                            db.Column('origin', db.Integer, db.ForeignKey('type.id')),
                            db.Column('opposing', db.Integer, db.ForeignKey('type.id')),
                            db.UniqueConstraint('origin', 'opposing', name='half_from_relation')
                            )

no_damage_to = db.Table('no_damage_to',
                        db.Column('id', db.Integer, primary_key=True),
                        db.Column('origin', db.Integer, db.ForeignKey('type.id')),
                        db.Column('opposing', db.Integer, db.ForeignKey('type.id')),
                        db.UniqueConstraint('origin', 'opposing', name='no_to_relation')
                        )

no_damage_from = db.Table('no_damage_from',
                          db.Column('id', db.Integer, primary_key=True),
                          db.Column('origin', db.Integer, db.ForeignKey('type.id')),
                          db.Column('opposing', db.Integer, db.ForeignKey('type.id')),
                          db.UniqueConstraint('origin', 'opposing', name='no_from_relation')
                          )


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

    primary_type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    secondary_type_id = db.Column(db.Integer, db.ForeignKey('type.id'))

    moves = db.relationship('Move', secondary=pokemon_move, backref=db.backref('pokemon', lazy='dynamic'))

    def dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = self.name.title()
        dictified['stats'] = [
            {
                'base_stat': self.speed,
                'name': 'speed'
            }, {
                'base_stat': self.special_defense,
                'name': 'special_defense'
            }, {
                'base_stat': self.special_attack,
                'name': 'special_attack'
            }, {
                'base_stat': self.defense,
                'name': 'defense'
            }, {
                'base_stat': self.attack,
                'name': 'attack'
            }, {
                'base_stat': self.hp,
                'name': 'hp'
            }
        ]
        dictified['primary_type'] = self.primary_type.id
        dictified['secondary_type'] = None if self.secondary_type is None else self.secondary_type.id
        dictified['average_stats'] = self.average_stats
        dictified['moves'] = [move.id for move in self.moves]

        return dictified

    def min_dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = self.name.title()
        dictified['primary_type'] = self.primary_type.id
        dictified['secondary_type'] = None if self.secondary_type is None else self.secondary_type.id
        dictified['average_stats'] = self.average_stats

        return dictified


class Move(db.Model):
    __tablename__ = 'move'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    accuracy = db.Column(db.Integer)
    pp = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    power = db.Column(db.Integer)
    damage_class = db.Column(db.String(80), nullable=False)

    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))

    def dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = str(self.name).title()
        dictified['accuracy'] = self.accuracy
        dictified['pp'] = self.pp
        dictified['priority'] = self.priority
        dictified['power'] = self.power
        dictified['damage_class'] = self.damage_class
        dictified['move_type'] = self.type_id
        dictified['pokemon'] = [pk.id for pk in self.pokemon]

        return dictified

    def min_dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = str(self.name).title()
        dictified['accuracy'] = self.accuracy
        dictified['pp'] = self.pp
        dictified['power'] = self.power
        dictified['move_type'] = self.type_id

        return dictified


class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    generation = db.Column(db.Integer)

    primary_types = db.relationship('Pokemon', backref='primary_type', lazy='dynamic',
                                    foreign_keys="[Pokemon.primary_type_id]")
    secondary_types = db.relationship('Pokemon', backref='secondary_type', lazy='dynamic',
                                      foreign_keys="[Pokemon.secondary_type_id]")
    moves = db.relationship('Move', backref='type', lazy='dynamic')

    double_damage_to = db.relationship('Type',
                                       secondary=double_damage_to,
                                       primaryjoin=id == double_damage_to.c.origin,
                                       secondaryjoin=id == double_damage_to.c.opposing,
                                       backref='double_damage_to_backref')

    double_damage_from = db.relationship('Type',
                                         secondary=double_damage_from,
                                         primaryjoin=id == double_damage_from.c.origin,
                                         secondaryjoin=id == double_damage_from.c.opposing,
                                         backref='double_damage_from_backref')

    half_damage_to = db.relationship('Type',
                                     secondary=half_damage_to,
                                     primaryjoin=id == half_damage_to.c.origin,
                                     secondaryjoin=id == half_damage_to.c.opposing,
                                     backref='half_damage_to_backref')

    half_damage_from = db.relationship('Type',
                                       secondary=half_damage_from,
                                       primaryjoin=id == half_damage_from.c.origin,
                                       secondaryjoin=id == half_damage_from.c.opposing,
                                       backref='half_damage_from_backref')

    no_damage_to = db.relationship('Type',
                                   secondary=no_damage_to,
                                   primaryjoin=id == no_damage_to.c.origin,
                                   secondaryjoin=id == no_damage_to.c.opposing,
                                   backref='no_damage_to_backref')

    no_damage_from = db.relationship('Type',
                                     secondary=no_damage_from,
                                     primaryjoin=id == no_damage_from.c.origin,
                                     secondaryjoin=id == no_damage_from.c.opposing,
                                     backref='no_damage_from_backref')

    def dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = str(self.name).title()
        dictified['generation'] = self.generation

        tables = [self.double_damage_to, self.double_damage_from, self.half_damage_to, self.half_damage_from,
                  self.no_damage_to, self.no_damage_from]
        table_names = ['double_damage_to', 'double_damage_from', 'half_damage_to', 'half_damage_from', 'no_damage_to',
                       'no_damage_from']

        for table, name in zip(tables, table_names):
            dictified[name] = [t.id for t in table]

        dictified['moves'] = [move.id for move in self.move_type]
        dictified['num_primary_type'] = len(self.pokemon_primary_type)
        dictified['num_secondary_type'] = len(self.pokemon_secondary_type)

        return dictified

    def min_dictify(self):
        dictified = OrderedDict()
        dictified['id'] = self.id
        dictified['name'] = str(self.name).title()
        dictified['generation'] = self.generation

        dictified['num_primary'] = len(self.primary_types.all())
        dictified['num_secondary'] = len(self.secondary_types.all())
        dictified['num_moves'] = len(self.moves.all())

        return dictified
