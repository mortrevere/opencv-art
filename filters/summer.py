from collections import deque
import numpy as np
import cv2 as cv


class SummerFilter:
    def __init__(self, rows, cols, size=3):
        self.rows = rows
        self.cols = cols
        self.size = size
        self._blank = np.full((self.rows, self.cols, 3), 0, dtype=np.uint8)
        self.queue = deque([self._blank.copy() for _ in range(self.size)])

    def compute(self, frame):
        out = self._blank.copy()
        c = 0
        self.queue.pop()
        self.queue.appendleft(frame)
        for f in self.queue:
            blur_size = (c % self.size + 1, c % self.size + 1)
            out += cv.blur(f, blur_size)
            c += 1
        return out
