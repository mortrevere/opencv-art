from collections import deque 
import numpy as np
import cv2 as cv
import math
from filter import Filter

class SlitScanFilter(Filter):
    def init(self):
        self.size = 50
        self.queue = deque([self._blank.copy() for _ in range(self.size)])

    def compute(self, frame):
        out = self._blank.copy()
        c = 0
        w = math.ceil(self.rows/self.size)
        self.queue.pop()
        self.queue.appendleft(frame)
        for f in self.queue:
            mask = self._mask.copy()
            pos = math.floor(c*w)
            cv.rectangle(mask,(0,pos),(self.cols,pos + w - 1),(255,255,255), -1)
            stripe = cv.bitwise_and(f,f,mask=mask)
            out = cv.bitwise_or(stripe, out)
            c += 1
        return out