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
        self.add_parameter("freq", bind="knob1", min=0.1, max=1, default=1)
        self.add_parameter("size", bind="fader1", min=4, max=int(self.rows/2), default=4)
        self.add_parameter("square", bind="button1s")
        self.add_parameter("black", bind="button1m")
        pass

    def compute(self, frame):
        lfo = 1
        o = 26
        color = (255, 255, 255)
        if self.black:
            color = (0,0,0)
        if random.random() > 1 - self.freq:
            x1 = random.randint(0, self.cols)
            y1 = random.randint(0, self.cols)
            if self.square:
                cv.rectangle(frame, (x1, y1), (x1 + int(self.size), y1 + int(self.size)), color, -1)
            else:
                cv.circle(frame, (x1, y1), int(self.size), color, -1)
        #cv.circle(frame, (int(self.cols/2 + lfo*self.scale - self.scale/2), int(self.rows/2  + o*self.scale - self.scale/2)),3, (255,255,255), -1)
        return frame
