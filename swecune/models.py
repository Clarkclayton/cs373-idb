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


class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    generation = db.Column(db.Integer)

    primary_types = db.relationship('Pokemon', backref='primary_type', lazy='dynamic')
    secondary_types = db.relationship('Pokemon', backref='secondary_type', lazy='dynamic')
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
