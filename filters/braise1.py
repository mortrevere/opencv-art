import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
from dice import Dice

class Braise1Filter(Filter):
    def init(self):
        self.m = Oscillator(1.618, zero=True)
        self.o = Oscillator(1/16, zero=True)
        self.c = Oscillator(0.1, zero=True)
        self.o2 = Oscillator(1/9, zero=True)
        self.M = np.float32([[1, 0, random.choice([2, -2, 0])], [0, 1, 0]])
        self.prev = self._blank.copy()
        self.i = 0
        self.reset = False
        self.max_channel_index = 0

        self.rect_w = Dice([5,1,1,-1])
        pass

    def compute(self, frame, vid=None):
        #return frame
        self.i += 1

        if self.i < 30:
            return self._blank
        #f = cv.addWeighted(frame,0.9,vid,0.1,0.0)
        f = cv.addWeighted(frame,0.5,self.prev,0.5,-5)
        #f = frame
        x1 = random.randint(0, self.cols)
        y1 = random.randint(0, self.rows)
        x2 = random.randint(0, int(self.cols/4))
        y2 = random.randint(0, int(self.rows/4))

        w = (random.randint(0, 1) * 2) - 1


        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        frame = cv.rectangle(f, (x1,y1), (x1 + x2,y1 + y2), (r,g,b), self.rect_w.next())
        

        bw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        non_zero = cv.countNonZero(bw)
        all_pixels = self.rows*self.cols
        occupation = non_zero/all_pixels
        #print(occupation)

        if occupation > 0.82 and random.random() > 0.8:
            frame = cv.rectangle(frame, (x1,0), (x1+x2,self.rows), (0,0,0), -1)

        if occupation > 0.50:
            avg = list(frame.mean(axis=0).mean(axis=0))
            max_val = max(avg)
            min_val = min(avg)
            self.max_channel_index = avg.index(max_val)
            frame[:,:,self.max_channel_index] = 127

        if occupation > 0.90:
            avg = list(frame.mean(axis=0).mean(axis=0))
            max_val = max(avg)
            min_val = min(avg)
            
            if not self.reset:
                self.max_channel_index = avg.index(max_val)
                self.reset = True
                self.encore = 4

        if self.reset and self.encore >= 0:
            frame[:,:,self.max_channel_index] = 0
            self.encore -= 1
            if self.encore == 0:
                self.reset = False

            
        self.prev = frame
        return f
        