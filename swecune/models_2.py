
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

    def __init__(self, id, name, hp, attack, defense, special_attack, special_defense, speed, average_stats):
        self.id = id
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.average_stats = average_stats


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

    def __init__(self, id, name, accuracy, pp, priority, power, damage_class):
        self.id = id,
        self.name = name,
        self.accuracy = accuracy,
        self.pp = pp,
        self.priority = priority,
        self.power = power,
        self.damage_class = damage_class


class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    generation = Column(Integer)

    move_type = relationship("Move", back_populates="type")

    double_damage_to = relationship('Type',
                                    secondary=double_damage_to,
                                    primaryjoin=id == double_damage_to.c.origin,
                                    secondaryjoin=id == double_damage_to.c.opposing,
                                    backref='double_damage_to_backref')

    double_damage_from = relationship('Type',
                                      secondary=double_damage_from,
                                      primaryjoin=id == double_damage_from.c.origin,
                                      secondaryjoin=id == double_damage_from.c.opposing,
                                      backref='double_damage_from_backref')

    half_damage_to = relationship('Type',
                                  secondary=half_damage_to,
                                  primaryjoin=id == half_damage_to.c.origin,
                                  secondaryjoin=id == half_damage_to.c.opposing,
                                  backref='half_damage_to_backref')

    half_damage_from = relationship('Type',
                                    secondary=half_damage_from,
                                    primaryjoin=id == half_damage_from.c.origin,
                                    secondaryjoin=id == half_damage_from.c.opposing,
                                    backref='half_damage_from_backref')

    no_damage_to = relationship('Type',
                                secondary=no_damage_to,
                                primaryjoin=id == no_damage_to.c.origin,
                                secondaryjoin=id == no_damage_to.c.opposing,
                                backref='no_damage_to_backref')

    no_damage_from = relationship('Type',
                                  secondary=no_damage_from,
                                  primaryjoin=id == no_damage_from.c.origin,
                                  secondaryjoin=id == no_damage_from.c.opposing,
                                  backref='no_damage_from_backref')