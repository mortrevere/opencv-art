from collections import deque 
import numpy as np
import cv2 as cv

class SlitScanFilter:
    def __init__(self, rows, cols, size=50):
        self.rows = rows
        self.cols = cols
        self.size = size
        self._blank = np.full((self.rows, self.cols, 3), 0, dtype=np.uint8)
        self._mask = np.full((self.rows, self.cols), 0, dtype=np.uint8)
        self.queue = deque([self._blank.copy() for _ in range(self.size)])
        print(f"SlitScanFilter initialized in {self.rows}x{self.cols}, {self.size} lines")

    def compute(self, frame):
        out = self._blank.copy()
        c = 0
        w = round(self.rows/self.size)
        self.queue.pop()
        self.queue.appendleft(frame)
        for f in self.queue:
            mask = self._mask.copy()
            pos = round(c*self.rows/self.size)
            

            cv.line(mask,(0,pos),(self.cols,pos),(255,255,255),w-1)
            stripe = cv.bitwise_and(f,f,mask=mask)
            out = cv.bitwise_or(stripe, out)
            c += 1
        return out