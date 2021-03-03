import math
import random

class Dice:
    def __init__(self, values, p=0.5, default=0):
        self.values = values
        self.zeroes = [default]*int(math.ceil(1/p)) if p != 1 else []
        self.all = self.values + self.zeroes
        print(f"Created a {len(self.all)}-faced dice")

    def next(self):
        return random.choice(self.all)
