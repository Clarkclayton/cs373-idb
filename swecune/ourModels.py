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
