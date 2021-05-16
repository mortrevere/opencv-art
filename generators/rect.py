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
        self.add_parameter("mouv_speed", bind="fader1", min=1, max=12, default=1)
        self.add_parameter("scale", bind="knob1", min=0, max=self.rows, default=200)
        self.add_parameter("sym", bind="button1s")
        self.reset()

    def reset(self):
        self.weights = [random.random() for i in range(self.mult)]
        self.divisions = sorted([int(x*self.cols) for x in self.weights])
        self.oscs = [Oscillator(freq=random.random(), zero=True) for i in range(self.mult)]
        '''
        divisions_acc = []
        sum_x = 0
        print(self.cols)
        for d in sorted(weights):
            print("d:", d)
            x1 = int(d*self.cols)
            print("x1:", x1)
            if len(divisions_acc) == 0:
                print("first one")
                divisions_acc += [x1]
            else:
                print("other")
                divisions_acc += [x1-divisions_acc[-1]]
            #print(divisions_acc)
        print(divisions)
        #self.divisions = divisions_acc
        '''

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
            cv.rectangle(frame, (x1, 0), (x2, int(osc*self.scale)), (255, 255, 255), 1)
            if self.sym:
                cv.rectangle(frame, (x1, self.rows), (x2, int(osc*self.scale)), (random.randint(0,255), random.randint(0,255), random.randint(0,255)), 3)
        
        return frame
