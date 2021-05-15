from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random
from oscillator import Oscillator
from dice import Dice

class PongFilter(Filter):
    def init(self):
        self.dx = random.randint(4, 10)
        self.sx = random.randint(0, self.cols)
        self.dy = random.randint(4, 10)
        self.sy = random.randint(0, self.rows)
        self.x = self.sx
        self.y = self.sy
        self.i = 0
        self.color = [255,255,255]
        self.size_osc = Oscillator(freq=14, zero=True)
        self.max_size = 6
        self.last_switch = 0

        self.max_size_dice = Dice(list(range(1,16)), p=1)
        self.direction_dice = Dice([1, -1], p=1/2)

        self.rot_osc = Oscillator(freq=1, zero=True)

        self.mode = 1
        pass

    def new_direction(self):
        #print(self.max_size)
        self.dy = random.randint(-1 * self.max_size - 3, self.max_size) + 3
        self.dx = random.randint(-1 * self.max_size - 3, self.max_size) + 3
        self.max_size = self.max_size_dice.next()
        self.size_osc.freq = self.max_size_dice.next()

    def compute(self, frame):
        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x > self.cols:
            self.dx *= -1
            self.max_size = self.max_size_dice.next()
            #self.color = (random.choice([0, 255]),random.choice([0, 255]),random.choice([0, 255]))
        if self.y < 0 or self.y > self.rows:
            self.dy *= -1
            self.max_size = self.max_size_dice.next()
            #self.color = (random.choice([0, 255]),random.choice([0, 255]),random.choice([0, 255]))
        radius = int(self.size_osc.next() * self.max_size) + 2
        #cv.rectangle(frame, (self.x, self.y), (self.x + radius, self.y + self.max_size), (255,255,255), -1)
        cv.circle(frame,(self.x, self.y),radius, (255,255,255), 1)
        return frame
