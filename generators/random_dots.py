from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random

class RandomDotsFilter(Filter):
    def init(self):
        self.scale = 200
        pass

    def compute(self, frame):
        lfo = 1
        o = 26
        if random.random() > 0.9:
            x1 = random.randint(0, self.cols)
            y1 = random.randint(0, self.cols)
            cv.circle(frame, (x1, y1), 4, (255, 255, 255), -1)
        cv.circle(frame, (int(self.cols/2 + lfo*self.scale - self.scale/2), int(self.rows/2  + o*self.scale - self.scale/2)),3, (255,255,255), -1)
        return frame
