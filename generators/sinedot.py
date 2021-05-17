from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random

class SineDotFilter(Filter):
    def init(self):
        self.osc = Oscillator(freq=1, zero=True)
        self.osc2 = Oscillator(freq=1/5, zero=True, phase=20)
        self.amplitude = 2
        self.add_parameter(name="circle_size", min=1, max=int(self.rows/2), bind="knob1")
        self.add_parameter(name="circle_fill", bind="button1m")
        self.add_parameter(name="scale", min=0, max=self.rows, default=int(self.rows/2), bind="fader1")
        self.add_parameter(name="speed", min=1/5, max=2, bind="knob2")

        self.color_osc = Oscillator(freq=1/3.09, zero=True)
        self.value_osc = Oscillator(freq=1/12, zero=True)

        self.direction = 1

        #self.scale = int(self.rows/2)

    def compute(self, frame):
        self.osc2.freq = self.speed

        lfo = self.osc2.next()
        self.osc.freq = lfo * 5
        o = self.osc.next()

        p = -1
        if self.circle_fill:
            p = 3

        cv.circle(frame, (int(self.cols/2 + lfo*self.scale - self.scale/2), int(self.rows/2  + o*self.scale - self.scale/2)),int(self.circle_size), (255,255,255), p)


        return frame
