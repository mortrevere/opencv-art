from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random

class GreyworldFilter(Filter):
    def init(self):
        self.osc = Oscillator(freq=1, zero=True)
        self.osc2 = Oscillator(freq=1/5, zero=True, phase=20)
        self.amplitude = 2
        self.add_parameter(name="gauss_amplitude", min=1, max=5, default=2.3, bind="fader3")
        self.add_parameter(name="gauss_baseline", min=0, max=100, default=100, bind="knob3")
        self.color_osc = Oscillator(freq=1/3.09, zero=True)
        self.value_osc = Oscillator(freq=1/2, zero=True)

        self.bird_osc = Oscillator(freq=1, zero=True)

        self.direction = 1

        self.scale = int(self.rows/2)
        self.i = 0
    def compute(self, frame):

        acc = frame
    
        if random.random() > 0.999:
            self.direction = -1*self.direction

        image_center = tuple(np.array(frame.shape[1::-1]) / 2)
        
        rot_matG = cv.getRotationMatrix2D(image_center, 0.1, 2-1.002)
        rot_matR = cv.getRotationMatrix2D(image_center, 0.5, 2-1.01)
        rot_matB = cv.getRotationMatrix2D(image_center, -0.72, 0.999)

        bird = self.bird_osc.next()
        if bird > 0.2 and bird < 0.5:
            acc[:,:,0] = cv.warpAffine(acc[:,:,0], rot_matR, frame.shape[1::-1], flags=cv.INTER_LINEAR)
        if bird < 0.2:
            acc[:,:,1] = cv.warpAffine(acc[:,:,1], rot_matG, frame.shape[1::-1], flags=cv.INTER_LINEAR)
        if bird > 0.5:
            acc[:,:,2] = cv.warpAffine(acc[:,:,2], rot_matB, frame.shape[1::-1], flags=cv.INTER_LINEAR)

        return acc - cv.GaussianBlur(frame, (0,0), self.gauss_amplitude) + int(self.gauss_baseline)
