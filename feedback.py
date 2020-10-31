import numpy as np
import cv2 as cv
from collections import deque 
import random
import time
import acapture

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
            blur_size = (c%self.size + 1, c%self.size + 1)
            out += cv.blur(f, blur_size)
            c += 1
        return out
        

class PerformanceWatcher:
    def __init__(self, buffer_size):
        self.observations = deque([0 for _ in range(buffer_size)])
    def observe(self, time):
        self.observations.pop()
        self.observations.appendleft(time)
    def get_time(self):
        return sum(self.observations)/len(self.observations)


cap = acapture.open(0)
ret, frame = cap.read()
rows, cols, depth = frame.shape

filter = SummerFilter(rows, cols)
perfs = PerformanceWatcher(10)

while True:
    t1 = time.time()
    ret, frame = cap.read()
    rows, cols, depth = frame.shape

    cv.imshow('frame', filter.compute(frame))
   
    if cv.waitKey(1) == ord('q'):
        break

    perfs.observe(time.time() - t1)

    print(perfs.get_time())

cap.release()
cv.destroyAllWindows()