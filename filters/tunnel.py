import numpy as np
import cv2 as cv
import math
from filter import Filter
from oscillator import Oscillator


class TunnelFilter(Filter):
    def init(self):
        self._previous = self._blank.copy()
        self.osc_h = Oscillator(freq=1, zero=True)
        self.osc_w = Oscillator(freq=1 / 3, zero=True, phase=42)
        self.osc_f = Oscillator(freq=1 / 7, zero=True, phase=42)

    def compute(self, frame):
        o_h = self.osc_h.next()
        o_w = self.osc_w.next()
        o_f = self.osc_f.next()
        # print(o)
        f = frame

        factor = o_f / 2 + 0.5
        h_translate = o_h * (self.cols * factor) / 8
        w_translate = o_w * (self.rows * factor) / 8
        # print(h_translate, w_translate)
        M = np.float32([[factor, 0, h_translate], [0, factor, w_translate]])
        # f = cv.warpAffine(f, M, (self.cols, self.rows))
        # f = self._previous + f
        # f = cv.bitwise_xor(f, self._previous)
        f = cv.addWeighted(f, 0.6, self._previous, 0.6, 0.0)

        self._previous = cv.warpAffine(f, M, (self.cols, self.rows))
        imghsv = cv.cvtColor(self._previous, cv.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv.split(imghsv)

        s = s * (10 * o_f)
        s = np.clip(s, 0, 255)
        imghsv = cv.merge([h, s, v])
        self._previous = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)
        return f
