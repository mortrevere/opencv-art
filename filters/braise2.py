import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
from dice import Dice

class Braise2Filter(Filter):
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
        self.x = random.randint(0, self.cols)
        self.y = random.randint(0, self.rows)
        self.dx = random.randint(-5, 5)
        self.dy = random.randint(-5, 5)

        self.color = (255,255,255)
        pass

    def compute(self, frame, vid=None):
        #return frame
        self.i += 1

        if self.i < 30:
            return self._blank
        #f = cv.addWeighted(frame,0.9,vid,0.1,0.0)
        f = cv.addWeighted(frame,0.8,self.prev,0.2,0)
        #f = frame
        
        bw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        non_zero = cv.countNonZero(bw)
        all_pixels = self.rows*self.cols
        occupation = non_zero/all_pixels
        #print(occupation)

        
        cv.rectangle(f, (self.x, self.y), (self.x + self.dx*10, self.y + self.dy*10), self.color, int(self.m.next()*10))
        #cv.circle(f, (self.x, self.y), 100, (255,255,255), int(self.m.next()*20))

        self.x += self.dx + 2
        self.y += self.dy + 1

        if random.random() > 0.90:
            self.x = random.randint(0, self.cols)
            self.y = random.randint(0, self.rows)
            self.dx = random.randint(-10, 10)
            self.dy = random.randint(-10, 10)
            if random.random() < 0.5:
                self.color = (0,0,0)
            else:
                self.color = (255,255,255)
        
        if occupation > 0.65:
            self.i = 25
            
            '''
            f = cv.cvtColor(cv.medianBlur(f, 3), cv.COLOR_BGR2GRAY)
            mask = cv.adaptiveThreshold(
                f, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 5, 8
            )
            invert_mask = 255 - mask
            '''

            #f = cv.bitwise_and(f, f, mask=invert_mask)
        
        #cv.circle(f, (self.x, self.y), 100, (255,255,255), int(self.m.next()*10))
        self.prev = f
        return f

        """ if occupation > 0.82 and random.random() > 0.8:
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
                self.reset = False """

            
        self.prev = frame
        return f
        