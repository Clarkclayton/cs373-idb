class Types():
    def __init__(self, ID, name, res, strong, im):
        self.ID = ID
        self.name = name
        self.resistance = res
        self.strength = strong
        self.immunity = im

class Pokemon():
    def __init__(self, ID, type1, type2, heldItem, encID, move, sprite, baseStats, evolvesInto, evolvesFrom):
        self.ID = ID
        self.pType1 = type1
        self.pType2 = type2
        self.heldItem = heldItem
        self.encounter = encID
        self.move = move
        self.sprite = sprite
        self.baseStats = baseStats
        self.evolvesInto = evolvesInto
        self.evolvesFrom = evolvesFrom

class Location():
    def __init__(self, ID, name, region)
        self.ID = ID
        self.name = name
        self.region = region

class Moves():
    def __init__(self, ID, acc, pp, prio, pwr, isSpecial, t)
        self.ID = ID
        self.accuracy = acc
        self.pp = pp
        self.priority = prio
        self.power = pwr
        self.isSpecial = isSpecial
        self.mType = t

class Item():
    def __init__(self, ID, name, cost, sprite, flavTxt)
        self.ID = ID
        self.name = name
        self.cost = cost
        self.sprite = sprite
        self.flavorText = flavTxt



