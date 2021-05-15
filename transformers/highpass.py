from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random

class HighpassFilter(Filter):
    def init(self):
        self.init = False
        self.i = 0
        self.mode = 0

    def compute(self, frame):
        if not self.init:
            self.center = frame.shape[1::-1]
            image_center = tuple(np.array(self.center) / 2)
            self.rot_mat = cv.getRotationMatrix2D(image_center, 0, 0.99)
            self.init = True

            self.rot_mat = []
            self.rot_mat += [cv.getRotationMatrix2D(image_center, 0.1, 2-1.002)]
            self.rot_mat += [cv.getRotationMatrix2D(image_center, 0.5, 2-1.01)]
            self.rot_mat += [cv.getRotationMatrix2D(image_center, -0.72, 0.999)]
        self.i += 1
        if self.mode == 1 and self.i%60 == 23:
            i = random.randint(0,2)
            frame[:,:,i] = cv.warpAffine(frame[:,:,i], self.rot_mat[i], self.center, flags=cv.INTER_LINEAR)
        
        return frame - cv.GaussianBlur(frame, (0,0), 1)
