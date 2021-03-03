import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
import time

class Gen2Filter(Filter):
    def init(self):
        self.color_osc = Oscillator(freq=1, zero=True)
        self.value_osc = Oscillator(freq=1/12, zero=True)
        self.width_osc = Oscillator(freq=6, zero=True)
        
        self.x = int(self.cols/2)
        self.y = int(self.rows/2)

        self.i = 0

    def compute(self, frame):

        self.i += 1

        frame = self._blank#.copy()

        color = int(self.color_osc.next()*179)
        rgb = cv.cvtColor(np.uint8([[[color, 255, 100 + int(self.value_osc.next()*155)]]]), cv.COLOR_HSV2BGR)
        color = rgb[0][0]
        color = (int(color[0]), int(color[1]), int(color[2]))

        cv.circle(frame, (self.x, self.y), int(self.width_osc.next()*self.rows), color, -1)

        
        if random.random() > 0.9:
            frame = cv.bitwise_and(frame, self._previous)
        #frame = cv.addWeighted(self._previous,0.5,frame,0.5,0.0)    
        self._previous = frame

        frame = cv.blur(frame, (2,2))
        
        time.sleep(1/60)
        return frame
