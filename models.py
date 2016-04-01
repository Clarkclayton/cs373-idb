from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import Table, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

pokemon_move = Table('pokemon_move', Base.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('pokemon_id', Integer, ForeignKey('pokemon.id')),
                     Column('move_id', Integer, ForeignKey('move.id')),
                     UniqueConstraint('pokemon_id', 'move_id', name='pokemon_move_relationship')
                     )

double_damage_to = Table('double_damage_to', Base.metadata,
                  Column('id', Integer, primary_key=True),
                  Column('origin', Integer, ForeignKey('type.id')),
                  Column('opposing', Integer, ForeignKey('type.id')),
                  UniqueConstraint('origin', 'opposing', name='double_to_relation')
                  )

double_damage_from = Table('double_damage_from', Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('origin', Integer, ForeignKey('type.id')),
                   Column('opposing', Integer, ForeignKey('type.id')),
                   UniqueConstraint('origin', 'opposing', name='double_from_relation')
                   )


half_damage_to = Table('half_damage_to', Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('origin', Integer, ForeignKey('type.id')),
                   Column('opposing', Integer, ForeignKey('type.id')),
                   UniqueConstraint('origin', 'opposing', name='half_to_relation')
                   )

half_damage_from = Table('half_damage_from', Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('origin', Integer, ForeignKey('type.id')),
                   Column('opposing', Integer, ForeignKey('type.id')),
                   UniqueConstraint('origin', 'opposing', name='half_from_relation')
                   )

no_damage_to = Table('no_damage_to', Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('origin', Integer, ForeignKey('type.id')),
                   Column('opposing', Integer, ForeignKey('type.id')),
                   UniqueConstraint('origin', 'opposing', name='no_to_relation')
                   )

no_damage_from = Table('no_damage_from', Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('origin', Integer, ForeignKey('type.id')),
                   Column('opposing', Integer, ForeignKey('type.id')),
                   UniqueConstraint('origin', 'opposing', name='no_from_relation')
                   )


class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    special_attack = Column(Integer)
    special_defense = Column(Integer)
    speed = Column(Integer)
    average_stats = Column(Integer)

    primary_type_id = Column(Integer, ForeignKey('type.id'))
    secondary_type_id = Column(Integer, ForeignKey('type.id'))

    primary_type = relationship('Type', backref='pokemon_primary_type', foreign_keys=[primary_type_id])
    secondary_type = relationship('Type', backref='pokemon_secondary_type', foreign_keys=[secondary_type_id])

    moves = relationship('Move', secondary=pokemon_move, back_populates='pokemon')


class Move(Base):
    __tablename__ = 'move'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    accuracy = Column(Integer)
    pp = Column(Integer)
    priority = Column(Integer)
    power = Column(Integer)
    damage_class = Column(String(80), nullable=False)

    type_id = Column(Integer, ForeignKey('type.id'))
    type = relationship('Type', back_populates='move_type')

    pokemon = relationship('Pokemon', secondary=pokemon_move, back_populates='moves')


class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    generation = Column(Integer)

    move_type = relationship("Move", back_populates="type")

    double_damage_to = relationship('Type',
                      secondary=double_damage_to,
                      primaryjoin=id==double_damage_to.c.origin,
                      secondaryjoin=id==double_damage_to.c.opposing,
                      backref='double_damage_to_backref')
    double_damage_from = relationship('Type', secondary=double_damage_from, primaryjoin=id==double_damage_from.c.origin, secondaryjoin=id==double_damage_from.c.opposing, backref='double_damage_from_backref')

    half_damage_to = relationship('Type', secondary=half_damage_to, primaryjoin=id==half_damage_to.c.origin, secondaryjoin=id==half_damage_to.c.opposing, backref='half_damage_to_backref')
    half_damage_from = relationship('Type', secondary=half_damage_from, primaryjoin=id==half_damage_from.c.origin, secondaryjoin=id==half_damage_from.c.opposing, backref='half_damage_from_backref')

    no_damage_to = relationship('Type', secondary=no_damage_to, primaryjoin=id==no_damage_to.c.origin, secondaryjoin=id==no_damage_to.c.opposing, backref='no_damage_to_backref')
    no_damage_from = relationship('Type', secondary=no_damage_from, primaryjoin=id==no_damage_from.c.opposing, secondaryjoin=id==no_damage_from.c.opposing, backref='no_damage_from_backref')



dialect = 'mysql+pymysql'
username = 'root'
password = '77corvette'
host = '127.0.0.1'
port = '3306'
database = 'SWECUNEDB'

engine = create_engine(
    "{}://{}:{}@{}:{}/{}".format(dialect, username, password, host, port, database)).connect()


# engine.execute('DROP TABLE IF EXISTS pokemon_move;')

# engine.execute('DROP TABLE IF EXISTS double_damage_to;')
# engine.execute('DROP TABLE IF EXISTS double_damage_from;')
# engine.execute('DROP TABLE IF EXISTS half_damage_to;')

# engine.execute('DROP TABLE IF EXISTS half_damage_from;')
# engine.execute('DROP TABLE IF EXISTS no_damage_to;')
# engine.execute('DROP TABLE IF EXISTS no_damage_from;')

# engine.execute('DROP TABLE IF EXISTS pokemon;')
# engine.execute('DROP TABLE IF EXISTS move;')
# engine.execute('DROP TABLE IF EXISTS type;')


# Base.metadata.create_all(engine)

# m = Move(name = 'test_move', accuracy = 1, pp = 2, prioirty = 3, power=4, damange_class = 'normal')
t1 = Type(name = 'name', generation=1)
t2= Type(name = 'name2', generation=1)
t3 = Type(name='name3', generation=2)

# t1.strengths.append(t2)
# t2.strengths.append(t1)

p = Pokemon(name='test1')
# m = Move(name='test2', damage_class='damage')
# p.moves.append(m)
p.primary_type = t3
p.secondary_type = t3



Session = sessionmaker(bind=engine)
session = Session()

# session.add(p)
session.commit()



# Base.metadata.create_all(connection)

# result = connection.execute('SELECT * FROM information_schema.tables;')
# print('\n\n')
# for row in result:
#     print(row)
# result = connection.execute('DESCRIBE pokemon;')

# print('\n\n')
# for row in result:
#     print(row)

# result = connection.execute('DESCRIBE move;')

# print('\n\n')
# for row in result:
#     print(row)

# result = connection.execute('DESCRIBE type;')

# print('\n\n')
# for row in result:
#     print(row)

# result = connection.execute('DESCRIBE pokemon_move;')

# print('\n\n')
# for row in result:
#     print(row)

# result = connection.execute('DESCRIBE strengths;')

# print('\n\n')
# for row in result:
#     print(row)

# result = connection.execute('DESCRIBE weaknesses;')

# print('\n\n')
# for row in result:
#     print(row)

# result = connection.execute('DESCRIBE immunities;')

# print('\n\n')
# for row in result:
#     print(row)
