from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random

class OccupationThresholdFilter(Filter):
    def init(self):
        self.latch = 0
        self.latch_inv = 0
        pass

    def compute(self, frame):
        bw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        non_zero = cv.countNonZero(bw)
        all_pixels = self.rows*self.cols
        occupation = non_zero/all_pixels

        

        if self.latch > 0:
            self.latch -= 1
        if self.latch_inv > 0:
            self.latch_inv -= 1

        if self.latch > 25:
            return self._blank
        if occupation > 0.99 and self.latch_inv == 0:
            self.latch = 30
            self.latch_inv = 300
            return self._blank
        if (occupation < 0.167 or occupation > 0.8) and self.latch == 0:
            pass
            #return cv.GaussianBlur(frame, (0,0), 3)
        
        
        return frame
        #return frame - cv.GaussianBlur(frame, (0,0), 1)
