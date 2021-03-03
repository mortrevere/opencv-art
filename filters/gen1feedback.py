import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
import time

class Gen1Filter(Filter):
    def init(self):
        self.x = random.randint(0, self.cols)
        self.y = random.randint(0, self.rows)

        self.dx = random.randint(1, 10)
        self.dy = random.randint(1, 10)
        
        self.i = 0
        self.latch = False

    def compute(self, frame):

        self.i += 1

        frame = self._blank
        

        if self.i%200 == 100:
            self.latch = True

        if self.latch:
            t = self.i/30
            self.y -= self.y/9
            self.y = round(self.y)
            print(self.y)
            if self.y < 50:
                self.latch = False

        cv.circle(frame, (self.x, self.y), 10, (255,255,255), -1)
        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x > self.cols:
            self.dx = -1*self.dx

        if self.y < 0 or self.y > self.rows:
            self.dy = -1*self.dy
        #frame = cv.addWeighted(self._previous,0.5,frame,0.5,0.0)    
        #self._previous = frame
        time.sleep(1/60)
        return frame
