from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random

class RectFilter(Filter):
    def init(self):
        #self.scale = 200
        self.mult = 15
        self.divisions = []
        self.oscs = []
        self.add_parameter("mouv_speed", bind="fader1", min=1, max=12, default=1, description="Speed of the bars")
        self.add_parameter("scale", bind="knob1", min=0, max=self.rows, default=200, description="Maximum height of bars (max = whole screen)")
        self.add_parameter("scale_colors", bind="knob2", min=0, max=1, default=1, description="Maximum height of colored bars")
        self.add_parameter("colors", bind="button2s", description="On/off color bars")
        self.add_parameter("fill", bind="button1m", description="Fill bars")
        self.add_parameter("fill_colors", bind="button2m", description="Fill color bars")
        self.reset()

    def reset(self):
        self.weights = [random.random() for i in range(self.mult)]
        self.divisions = sorted([int(x*self.cols) for x in self.weights])
        self.oscs = [Oscillator(freq=random.random(), zero=True) for i in range(self.mult)]

    def compute(self, frame):
        
        for i in range(self.mult):
            self.oscs[i].freq = self.weights[i]*self.mouv_speed
            if i == 0:
                x1 = 0
                x2 = self.divisions[0]
            else:
                x1 = self.divisions[i-1]
                x2 = self.divisions[i]
            #print(x1, x2)
            osc = self.oscs[i].next()
            p = 1
            if self.fill:
                p = -1
            cv.rectangle(frame, (x1, 0), (x2, int(osc*self.scale)), (255, 255, 255), p)
            
            #print(self.scale_colors)
            if self.colors:
                p = 1
                if self.fill_colors:
                    p = -1
                cv.rectangle(frame, (x1, self.rows), (x2, int((osc*self.scale)+self.rows*(1-self.scale_colors))), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), p)
        
        return frame
