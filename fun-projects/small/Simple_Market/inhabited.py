import random
import math

raw_goods_list = ["Wheat", "Timber", "Iron Ore", "Wool", "Stone", "Fish", "Hides", "Clay", "Copper Ore", "Flax"]

class population_centre():
    #initialise the object with base parameters
    def __init__(self, x, y, currency, population):
        self.x = x
        self.y = y
        self.currency = currency
        self.population = population
        self.inventory = 0.0

class Village(population_centre):
    def __init__(self,x , y, currency, population):
        super().__init__(x, y, currency, population)
        self.good_type = random.choice(raw_goods_list)

    def produce_good(self):
        self.inventory += self.population * 1.3

    def consumption(self):
        self.inventory -= (self.population * .3)
        self.population += math.ceil(self.population * .1)

    def check_promote(self, current_city_exists = False):
        if self.population >= 500:
            print(f"Village located at ({self.x}, {self.y}) has changed into a Town!")
            new_town = Town(self.x, self.y, self.currency, self.population)
            new_town.inventory = self.inventory
            return new_town
        return self

class Town(population_centre):
    def __init__(self, x, y, currency, population):
        super().__init__(x,y, currency, population)
        self.payout_per_unit = 5.0
        self.expansion_cooldown = 0

    def produce_good(self):
        base_farm = max(10, 200 - (self.population * 0.2))
        self.inventory += base_farm

    def consumption(self):
        self.inventory -= (self.population * .3)
        self.population += math.ceil(self.population * .1)

    def expansion(self, settlements, screen_width = 800, screen_height = 600):
        if self.expansion_cooldown > 0:
            self.expansion_cooldown -= 1
            return None
        if self.population >= 750:
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(100, 200)
            candidate_x = self.x + math.cos(angle) * dist
            candidate_y = self.y + math.sin(angle) * dist

            if 50 <= candidate_x <= screen_width - 50 and 50 <= candidate_y <= screen_height - 50:
                            # Ensure no other settlement is within 50 pixels of candidate location
                is_clear = True
                for s in settlements:
                    if math.hypot(s.x - candidate_x, s.y - candidate_y) < 50:
                        is_clear = False
                        break

                if is_clear:
                    self.population -= 50
                    print(f"Town at ({self.x}, {self.y}) sent out a Pioneer!")
                    return (candidate_x, candidate_y)
                return None

    def check_promote(self, current_city_exists):
        if self.population >= 1500 and not current_city_exists:
            print(f"Town at ({self.x}, {self.y}) evolved into THE Capital!")
            new_city = City(self.x, self.y, self.currency, self.population)
            new_city.inventory = self.inventory
            return new_city
        return self

class City(population_centre):
    def __init__(self, x, y, currency, population):
        super().__init__(x,y, currency, population)
        self.payout_per_unit = 10.0

    def check_promote(self, current_city_exists):
        return self
