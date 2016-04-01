"""
Model for Pokemon.
This represents the metadata relating to a given Pokemon.
There exists a many to 1..2 relationship from Pokemon to Type.
There exists a many to many relationship from Pokemon to Move.
"""


class Pokemon():
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
        return Pokemon(id=1, name="Foo", hp=1, attack=1, defense=1, special_attack=1, special_defense=1, speed=1, average_stats=1, primary_type=None, secondary_type=None, moves=[2])


"""
Model for Move.
This represents the metadata relating to a given Move that pokemon can have.
There exists a 1 to many relationship from Type to Move.
There exists a many to many relationship from Move to Pokemon.
"""


class Move():
    def __init__(self, id, name, accuracy, pp, priority, power, damage_class, move_type):
        self.id = id
        self.name = name
        self.accuracy = accuracy
        self.pp = pp
        self.priority = priority
        self.power = power
        self.damage_class = damage_class
        self.move_type = move_type

    @staticmethod
    def get_move(id):
        return Move(id=1, name="bitch slap", accuracy=100, pp=50, priority=0, power=50, damage_class="special", move_type=1)


"""
Model for Type.
This represents the metadata relating to a given Type that a Pokemon and Move can have.
There exists a many to many relationship from Type to Type.
There exists a 1..2 to many relationship from Type to Pokemon.
There exists a 1 to many relationship from Type to Move.
"""


class Type():
    def __init__(self, id, name, generation, immunities, strengths, weaknesses):
        self.id = id
        self.name = name
        self.generation = generation
        self.immunities = immunities
        self.strengths = strengths
        self.weaknesses = weaknesses

    @staticmethod
    def get_type(id):
        return Type(id=1, name="Fire", generation=1, immunities=[1, 2], strengths=[3, 4], weaknesses=[5, 6])
