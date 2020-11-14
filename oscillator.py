import math


class Oscillator:
    def __init__(self, freq, phase=0, zero=False):
        self.freq = freq
        self.phase = phase
        self.zero = zero
        self.tick = 0

    def next(self):
        self.tick += 1 / 360
        o = math.cos(2 * math.pi * self.freq * self.tick + self.phase / 360) + (1 if self.zero else 0)
        return o / 2 if self.zero else o
