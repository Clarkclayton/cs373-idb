from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, pd):
        print(pd['id'])


class Types(Base):
    def __init__(self, pd):
        super().__init__(pd)
        self.ID = pd['id']
        self.name = pd['name']
        self.resistance = None  # TODO: Which ones are these?
        self.strength = None  # TODO: Which ones are these?
        self.immunity = None  # TODO: Which ones are these?
        self.generation = id_from_url(pd['generation']['url'])


class Pokemon(Base):
    def __init__(self, pd):
        super().__init__(pd)
        self.ID = pd['id']
        self.name = pd['name']
        # self.pType1 = id_from_url(pd['types'][0]['type']['url'])  # TODO: Do we want to completely normalize this?
        # self.pType2 = id_from_url(pd['types'][1]['type']['url']) if len(pd['types']) > 1 else None
        # for static page
        self.pType1 = pd['types'][0]['type']['name']  # TODO: Do we want to completely normalize this?
        self.pType2 = pd['types'][1]['type']['name'] if len(pd['types']) > 1 else None
        self.heldItem = []  # TODO: fix this
        self.encounter = []  # TODO: fix this
        self.moves = [id_from_url(move['move']['url']) for move in pd['moves']]
        self.sprite = pd['sprites']['front_default']
        self.baseStats = {st['stat']['name']: st['base_stat'] for st in pd['stats']}
        self.averageStats = round(sum(int(x) for x in self.baseStats.values()) / len(self.baseStats.keys()))
        self.evolvesInto = None  # TODO: fix this
        self.evolvesFrom = None  # TODO: fix this
        self.pTypeId1 = int(pd['types'][0]['type']['url'].split('/')[-2])
        self.pTypeId2 = int(pd['types'][1]['type']['url'].split('/')[-2]) if len(pd['types']) > 1 else None

        if pd['types'][0]['slot'] != 1:
            self.pType1, self.pType2 = self.pType2, self.pType1
            self.pTypeId1, self.pTypeId2 = self.pTypeId2, self.pTypeId1

class Moves(Base):
    def __init__(self, pd):
        super().__init__(pd)
        self.ID = pd['id']
        self.name = pd['name']
        self.accuracy = pd['accuracy']
        self.pp = pd['pp']
        self.priority = pd['priority']
        self.power = pd['power']
        self.dmg_class = pd['damage_class']['name']
        self.m_type = pd['type']['name']
        self.m_type_id = int(pd['type']['url'].split('/')[-2])


def id_from_url(full_url):
    return full_url.split('/')[-2]
