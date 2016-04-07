from unittest import TestCase

from models import Pokemon, Type, Move
from swecune.server import db

class tests(TestCase):
    normal_type = Type(id=1, name="normal", generation=1, immunities=[], strengths=[], weaknesses=[])
    grass_type = Type(id=12, name="grass", generation=1, immunities=[], strengths=[], weaknesses=[])
    poison_type = Type(id=4, name="poison", generation=1, immunities=[], strengths=[], weaknesses=[])
    tackle_move = Move(id=33, name="tackle", accuracy=100, pp=35, priority=0, power=50, damage_class="physical", move_type=normal_type)
    pokemon = Pokemon(id=1, name="bulbasaur", hp=45, attack=49, defense=49, special_attack=65, special_defense=65, speed=45, average_stats=53, primary_type=grass_type, secondary_type=poison_type, moves=[tackle_move])

	#Tests that Pokemon Table is writable
	def test_pokemon_writable(self):
        numPokeBeforeWrite = len(Pokemon.query.all())

        db.session.add(pokemon)
        db.session.commit()

        numPokeAfterWrite = len(Pokemon.query.all())

        self.assertEqual(numPokeBeforeWrite + 1, numPokeAfterWrite)

    #Tests that Pokemon Table is readable
    def test_pokemon_readable(self):
        db.session.add(pokemon)
        db.session.commit()

        bulbasaur = Pokemon.query.get(1)

        self.assertEqual(bulbasaur.id, 1)
        self.assertEqual(bulbasaur.name, "bulbasaur")
        self.assertEqual(bulbasaur.hp, 45)
        self.assertEqual(bulbasaur.attack, 49)
        self.assertEqual(bulbasaur.defense, 49)
        self.assertEqual(bulbasaur.special_attack, 65)
        self.assertEqual(bulbasaur.special_defense, 65)
        self.assertEqual(bulbasaur.speed, 45)
        self.assertEqual(bulbasaur.average_stats, 53)

    #Tests that Pokemon Table is deletable
    def test_pokemon_deletable(self):
        db.session.add(pokemon)
        db.session.commit()

        numPokeAfterWrite = len(Pokemon.query.all())

        db.session.delete(pokemon)
        db.session.commit()

        numPokeAfterDelete = len(Pokemon.query.all())

        self.assertEqual(numPokeAfterWrite - 1, numPokeAfterDelete)

    #Tests that Type Table is writeable
    def test_type_writeable(self):
        numTypesBeforeWrite = len(Type.query.all())

        db.session.add(grass_type)
        db.session.commit()

        numTypesAfterWrite = len(Type.query.all())

        self.assertEqual(numTypesBeforeWrite + 1, numTypesAfterWrite)

    #Tests that Type Table is readable
    def test_type_readable(self):
        db.session.add(pokemon)
        db.session.commit()

        grass_t = Type.query.get(12)

        self.assertEqual(grass_t.id, 12)
        self.assertEqual(grass_t.name, "grass")
        self.assertEqual(grass_t.generation, 1)
        self.assertEqual(grass_t.immunities, [])
        self.assertEqual(grass_t.strengths, [])
        self.assertEqual(grass_t.weaknesses, [])

    #Tests that Type Table is deleteable
    def test_type_deletable(self):
        db.session.add(grass_type)
        db.session.commit()

        numTypesAfterWrite = len(Type.query.all())

        db.session.delete(grass_type)
        db.session.commit()

        numTypesAfterDelete = len(Type.query.all())

        self.assertEqual(numTypesAfterWrite - 1, numTypesAfterDelete)

    #Tests that Move Table is writeable
    def test_move_writable(self):
        numMovesBeforeWrite = len(Move.query.all())

        db.session.add(tackle_move)
        db.session.commit()

        numMovesAfterWrite = len(Move.query.all())

        self.assertEqual(numMovesBeforeWrite + 1, numMovesAfterWrite)

    #Tests that Move Table is readable
    def test_move_readable(self):
        db.session.add(tackle_move)
        db.session.commit()

        tackle_m = Move.query.get(33)

        self.assertEqual(tackle_m.id, 33)
        self.assertEqual(tackle_m.name, "tackle")
        self.assertEqual(tackle_m.accuracy, 100)
        self.assertEqual(tackle_m.pp, 35)
        self.assertEqual(tackle_m.priority, 0)
        self.assertEqual(tackle_m.power, 50)
        self.assertEqual(tackle_m.damage_class, "physical")

    #Tests that Move Table is deleteable
    def test_move_deleteable(self):
        db.session.add(tackle_move)
        db.session.commit()

        numMovesAfterWrite = len(Move.query.all())

        db.session.delete(tackle_move)
        db.session.commit()

        numMovesAfterDelete = len(Move.query.all())

        self.assertEqual(numMovesAfterWrite - 1, numMovesAfterDelete)
