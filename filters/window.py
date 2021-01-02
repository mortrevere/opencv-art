import numpy as np
import cv2 as cv
import math
from filter import Filter
from oscillator import Oscillator
import random


class WindowFilter(Filter):
    def init(self):
        self._mask = np.full((self.rows, self.cols), 0, dtype=np.uint8)
        self.o1 = Oscillator(freq=5, zero=True)
        self.o2 = Oscillator(freq=7, zero=True)
        self.o3 = Oscillator(freq=5, zero=True)
        self.o = 0
        self.count = 0
        pass

    def compute(self, frame):
        n = int(self.o1.next() * 7 + 2)
        # o = (self.o1.next() * n * n)
        # if o*o > 0.7:
        o = random.randint(0, n * n)
        self.count += 1
        if self.count % 7 == 0:
            self.o = o
        rect = []
        for i in range(n):
            for j in range(n):
                w0 = int(i * (self.rows / n))
                h0 = int(j * (self.cols / n))
                # print(((1+i)*(self.rows/n),(1+j)*(self.cols/n)))
                w1 = int((1 + i) * (self.rows / n)) - 1 + int(self.o2.next() * 80)
                h1 = int((1 + j) * (self.cols / n)) - 1 + int(self.o1.next() * 40)
                # pass
                r = self._mask.copy()
                cv.rectangle(r, (h0, w0), (h1, w1), (255, 255, 255), -1)
                # frame = cv.rectangle(self._blank.copy(), (0,0), (100,200), 0, -1)
                # rect += [cv.cvtColor(r, cv.COLOR_GRAY2BGR)]
                rect += [r]
        i = 1
        out = self._blank.copy()
        (r, _, _) = cv.split(frame)
        framebw = cv.merge((r, r, r))
        for r in rect:
            if int(self.o) == i:
                out += cv.bitwise_xor(255 - frame, out, mask=r)
            else:
                pass
                if random.random() > 0.7:
                    out += cv.bitwise_and(frame, frame, mask=r)
            i += 1
        # qframe += rect[0]
        return out
