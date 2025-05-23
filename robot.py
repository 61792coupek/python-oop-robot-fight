import random

class Robot:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.energy = 100
        self.attack_power = 10

    def check_hp(self):
        return f"Robot: {self.name}\nPočet HP: {self.hp}\nEnergie: {self.energy}"
    