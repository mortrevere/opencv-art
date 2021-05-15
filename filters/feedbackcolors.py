import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
from dice import Dice

class FeedbackColorsFilter(Filter):
    def init(self):
        self.color_osc = Oscillator(freq=0.423, zero=True)
        self.value_osc = Oscillator(freq=1/12, zero=True)
        self.width_osc = Oscillator(freq=1, zero=True)

        self.attacker_osc = Oscillator(freq=1.76, phase=12, zero=True)
        self.attacker_coords = None

        self.half_width = int(self.cols/2)
        self.half_height = int(self.rows/2)

        self.quarter_height = int(self.rows/4)
        self.quarter_width = int(self.cols/4)

        self.wiggle = Dice([-1, 1], p=1/500)

        self.i = 0

        self.mode = 0
        pass

    def compute(self, frame, vid=None):
        self.i += 1
        if self.i < 30:
            return self._blank
        
        color = int(self.color_osc.next()*179)
        rgb = cv.cvtColor(np.uint8([[[color, 255, 100 + int(self.value_osc.next()*155)]]]), cv.COLOR_HSV2BGR)
        color = rgb[0][0]
        color = (int(color[0]), int(color[1]), int(color[2]))
        
        cv.line(frame,(self.half_width,0),(self.half_width,self.rows),color,int(self.width_osc.next()*16)+4)

        if self.attacker_osc.next() < (self.mode + 1)*0.1 and random.random() < 0.1:
            #if self.attacker_coords is None:
            self.attacker_coords = [(random.randint(0,self.quarter_width),random.randint(0,self.rows)),
                                    (random.randint(0,self.quarter_width),random.randint(0,self.rows))]
            #cv.line(frame,self.attacker_coords[0], self.attacker_coords[1],(255,255,255),4)
            cv.circle(frame,self.attacker_coords[0], random.randint(8, 16),(255,255,255),-1)

            if self.mode == 0:
                color = (0,0,0)
            if random.random() < 0.5:
                cv.rectangle(frame, (0,0), (self.cols, self.rows), color, 16)
                if self.mode == 1:
                    f = cv.bitwise_or(frame, self._previous)
                    self._previous = f
                    return f
        else:
            self.attacker_coords = None

        bw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        non_zero = cv.countNonZero(bw)
        all_pixels = self.rows*self.cols
        occupation = non_zero/all_pixels
        if self.attacker_osc.next() > 0.99 and occupation > 0.99999:
            f = self._blank.copy()
            self._previous = f
            return f

        if self._previous is not None:
            frame = cv.addWeighted(frame,0.5,self._previous,0.5,0.0)

        zoom = 0.01
        M = np.float32([[1, 0, self.wiggle.next()], [0, 1, 0]])
        frame = cv.warpAffine(frame, M, (self.cols, self.rows))

        self._previous = frame
        return frame
