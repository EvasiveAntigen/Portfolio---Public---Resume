import random
import math

raw_goods_list = ["Wheat", "Timber", "Iron Ore", "Wool", "Stone", "Fish", "Hides", "Clay", "Copper Ore", "Flax"]

class population_centre():
    #initialise the object with base parameters
    def __init__(self, currency, population):
        self.currency = currency
        self.population = population
        self.inventory = 0

class Village(population_centre):
    def __init__(self, currency, population):
        super().__init__(currency, population)
        self.good_type = random.choice(raw_goods_list)

    def produce_good(self):
        self.inventory += self.population * 1.3

    def consumption(self):
        self.inventory -= (self.population * .3)
        self.population += math.ceil(self.population * .1)

class Town():
    pass

class City():
    pass
