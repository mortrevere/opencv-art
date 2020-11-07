from collections import deque 
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter

class DragFilter(Filter):
    def init(self):
        self.osc = Oscillator(freq=1)
        self.osc2 = Oscillator(freq=5, zero=True, phase=20)
        self.amplitude = 0
        self.add_parameter(name="amplitude", min=10, max=60)

    def compute(self, frame):
        f = cv.cvtColor(cv.medianBlur(frame,3), cv.COLOR_BGR2GRAY)
        mask = cv.adaptiveThreshold(f, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,17,4)
        invert_mask = 255 - mask

        source = cv.bitwise_and(frame,frame, mask=invert_mask)
        lfo = self.osc2.next()
        self.osc.freq = lfo*5
        o = self.osc.next()
        print(self.amplitude)
        self.M = np.float32([[1,0,self.amplitude],[0,1,self.amplitude]])

        acc = cv.addWeighted(self._previous, 0.9, cv.warpAffine(source,self.M,(self.cols,self.rows)), 1, 0.0)
        self._previous = acc
        #invert_frame = cv.bitwise_not(frame)
        #acc = cv.bitwise_or(acc, cv.bitwise_and(invert_frame, invert_frame, mask=invert_mask))
        
        return acc