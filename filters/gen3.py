import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
import time

class Gen3Filter(Filter):
    def init(self):
        self.color_osc = Oscillator(freq=1, zero=True)
        self.value_osc = Oscillator(freq=1/12, zero=True)
        self.width_osc = Oscillator(freq=6, zero=True)
        
        self.x = int(self.cols/2)
        self.y = int(self.rows/2)

        self.i = 0

    def compute(self, frame):

        self.i += 1

        #frame = cv.Canny(frame,100,128)
        #frame = cv.merge([frame, frame, frame])
        #frame = cv.bitwise_xor(frame, self._previous)
        #frame = cv.dft(frame)
        f = np.float32(frame)
        print(f.shape)
        dft = cv.dft(f,flags = cv.DFT_COMPLEX_OUTPUT)
        print(dft.shape)
        dft_shift = np.fft.fftshift(dft)


        #if self._previous is not None:
        #    frame = cv.addWeighted(frame,0.5,self._previous,0.5,0.0)
        #self._previous = frame

        return np.uint8(dft_shift)
