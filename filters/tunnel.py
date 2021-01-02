import numpy as np
import cv2 as cv
import math
from filter import Filter
from oscillator import Oscillator


class TunnelFilter(Filter):
    def init(self):
        self._previous = self._blank.copy()
        self.osc_h = Oscillator(freq=1 / 7)
        self.osc_w = Oscillator(freq=5 / 3, phase=42)
        self.osc_f = Oscillator(freq=3, phase=42)
        self.osc_sign1 = Oscillator(zero=True, freq=1 / 6)
        self.osc_sign2 = Oscillator(freq=17, phase=77)

    def compute(self, frame):
        m = self.osc_sign1.next()
        o_h = self.osc_h.next() / 20
        o_w = self.osc_w.next() / 20

        # adds zooms
        o_f = (self.osc_f.next() * (1 - m)) + m
        # o_f = self.osc_f.next() * 0.02 + 0.95

        f = frame.copy()

        factor = o_f
        # adds wiggling
        h_translate = (1 - o_f) / 2 * self.cols + o_h * 120
        w_translate = (1 - o_f) / 2 * self.rows + o_w * 170
        M = np.float32([[factor, 0, h_translate], [0, factor, w_translate]])
        f = cv.bitwise_xor(f, self._previous)

        self._previous = cv.warpAffine(f, M, (self.cols, self.rows))

        imghsv = cv.cvtColor(self._previous, cv.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv.split(imghsv)
        s = s * (10 * o_f)
        s = np.clip(s, 0, 255)
        v = v / 1.01
        # WOOT
        s, v = v, s
        h = h / 1.1
        imghsv = cv.merge([h, s, v])

        self._previous = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)
        # self._previous = cv.blur(self._previous, (2, 1))
        # f = cv.bitwise_xor(f, frame)
        return f
