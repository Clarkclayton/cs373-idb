from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, pd):
        print (pd['id'])


class Types(Base):
    def __init__(self, pd):
        super().__init__(pd)
        self.ID = pd['id']
        self.name = pd['name']
        self.resistance = None  # TODO: Which ones are these?
        self.strength = None  # TODO: Which ones are these?
        self.immunity = None  # TODO: Which ones are these?


class Pokemon(Base):
    def __init__(self, pd):
        super().__init__(pd)
        self.ID = pd['id']
        self.pType1 = id_from_url(pd['types'][0]['type']['url'])  # TODO: Do we want to completely normalize this?
        self.pType2 = id_from_url(pd['types'][1]['type']['url']) if len(pd['types']) > 1 else None
        self.heldItem = []  # TODO: fix this
        self.encounter = []  # TODO: fix this
        self.move = [id_from_url(move['move']['url']) for move in pd['moves']]
        self.sprite = pd['sprites']['front_default']
        self.baseStats = None  # TODO: fix this
        self.evolvesInto = None  # TODO: fix this
        self.evolvesFrom = None  # TODO: fix this


class Location(Base):
    def __init__(self, pd):
        super().__init__(pd)
        self.ID = pd['id']
        self.name = find_english_version(pd['names'], 'name')
        self.region = id_from_url(pd['region']['url']) if pd['region'] is not None else None


class Moves(Base):
    def __init__(self, pd):
        super().__init__(pd)
        self.ID = pd['id']
        self.accuracy = pd['accuracy']
        self.pp = pd['accuracy']
        self.priority = pd['priority']
        self.power = pd['power']
        self.is_special = False  # TODO: Where is this listed?
        self.m_type = id_from_url(pd['type']['url'])


class Item(Base):
    def __init__(self, pd):
        super().__init__(pd)
        self.ID = pd['id']
        self.name = pd['name']
        self.cost = pd['cost']
        self.sprite = pd['sprites']['default']
        self.flavor_text = find_english_version(pd['flavor_text_entries'], 'text')


def find_english_version(list_entries, key_attr):
    for item in list_entries:
        if item['language']['name'] == 'en':
            return item[key_attr]


def id_from_url(full_url):
    return full_url.split('/')[-2]
