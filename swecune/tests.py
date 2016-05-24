from unittest import main, TestCase

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import username, password, host, port, database
from models import Pokemon, Move, Type


class tests(TestCase):
    def setUp(self):
        try:
            SQLALCHEMY_DATABASE_URI_TEMP = '{engine}://{username}:{password}@{hostname}:{port}/{database}'.format(
                engine='mysql+pymysql',
                username=username,
                password=password,
                hostname=host,
                port=port,
                database=database)

            self.app = Flask(__name__)
            self.app.debug = True
            self.app.config['SQLALCHEMY_ECHO'] = True
            self.app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI_TEMP
            self.app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            self.db = SQLAlchemy(self.app)
        except:
            pass

    def test_pokemon_1_readable(self):
        with self.app.app_context():
            test_pk = Pokemon.query.get(1)

        self.assertEqual(test_pk.id, 1)
        self.assertEqual(test_pk.name, "bulbasaur")
        self.assertEqual(test_pk.hp, 45)
        self.assertEqual(test_pk.attack, 49)
        self.assertEqual(test_pk.defense, 49)
        self.assertEqual(test_pk.special_attack, 65)
        self.assertEqual(test_pk.special_defense, 65)
        self.assertEqual(test_pk.speed, 45)
        self.assertEqual(test_pk.average_stats, 53)

    def test_pokemon_2_readable(self):
        with self.app.app_context():
            test_pk = Pokemon.query.get(2)

        self.assertEqual(test_pk.id, 2)
        self.assertEqual(test_pk.name, "ivysaur")
        self.assertEqual(test_pk.hp, 60)
        self.assertEqual(test_pk.attack, 62)
        self.assertEqual(test_pk.defense, 63)
        self.assertEqual(test_pk.special_attack, 80)
        self.assertEqual(test_pk.special_defense, 80)
        self.assertEqual(test_pk.speed, 60)
        self.assertEqual(test_pk.average_stats, 67)

    def test_pokemon_3_readable(self):
        with self.app.app_context():
            test_pk = Pokemon.query.get(4)

        self.assertEqual(test_pk.id, 4)
        self.assertEqual(test_pk.name, "charmander")
        self.assertEqual(test_pk.hp, 39)
        self.assertEqual(test_pk.attack, 52)
        self.assertEqual(test_pk.defense, 43)
        self.assertEqual(test_pk.special_attack, 60)
        self.assertEqual(test_pk.special_defense, 50)
        self.assertEqual(test_pk.speed, 65)
        self.assertEqual(test_pk.average_stats, 51)

    def test_pokemon_4_readable(self):
        with self.app.app_context():
            test_pk = Pokemon.query.get(25)

        self.assertEqual(test_pk.id, 25)
        self.assertEqual(test_pk.name, "pikachu")
        self.assertEqual(test_pk.hp, 35)
        self.assertEqual(test_pk.attack, 55)
        self.assertEqual(test_pk.defense, 40)
        self.assertEqual(test_pk.special_attack, 50)
        self.assertEqual(test_pk.special_defense, 50)
        self.assertEqual(test_pk.speed, 90)
        self.assertEqual(test_pk.average_stats, 53)

    def test_move_physical_readable(self):
        with self.app.app_context():
            test_move = Move.query.get(1)

        self.assertEqual(test_move.id, 1)
        self.assertEqual(test_move.name, "pound")
        self.assertEqual(test_move.accuracy, 100)
        self.assertEqual(test_move.pp, 35)
        self.assertEqual(test_move.priority, 0)
        self.assertEqual(test_move.power, 40)
        self.assertEqual(test_move.damage_class, "physical")

    def test_move_special_readable(self):
        with self.app.app_context():
            test_move = Move.query.get(59)

        self.assertEqual(test_move.id, 59)
        self.assertEqual(test_move.name, "blizzard")
        self.assertEqual(test_move.accuracy, 70)
        self.assertEqual(test_move.pp, 5)
        self.assertEqual(test_move.priority, 0)
        self.assertEqual(test_move.power, 110)
        self.assertEqual(test_move.damage_class, "special")

    def test_move_sword_attack_readable(self):
        with self.app.app_context():
            test_move = Move.query.get(14)

        self.assertEqual(test_move.id, 14)
        self.assertEqual(test_move.name, "swords-dance")
        self.assertEqual(test_move.accuracy, None)
        self.assertEqual(test_move.pp, 20)
        self.assertEqual(test_move.priority, 0)
        self.assertEqual(test_move.power, None)
        self.assertEqual(test_move.damage_class, "status")

    def test_type_first_generation_readable(self):
        with self.app.app_context():
            test_type = Type.query.get(10)

        self.assertEqual(test_type.id, 10)
        self.assertEqual(test_type.name, "fire")
        self.assertEqual(test_type.generation, 1)

    def test_type_second_generation_readable(self):
        with self.app.app_context():
            test_type = Type.query.get(9)

        self.assertEqual(test_type.id, 9)
        self.assertEqual(test_type.name, "steel")
        self.assertEqual(test_type.generation, 2)

    def test_type_sixth_generation_readable(self):
        with self.app.app_context():
            test_type = Type.query.get(18)

        self.assertEqual(test_type.id, 18)
        self.assertEqual(test_type.name, "fairy")
        self.assertEqual(test_type.generation, 6)


if __name__ == "__main__":
    main()
