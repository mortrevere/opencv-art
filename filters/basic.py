import numpy as np
import cv2 as cv
import math
from filter import Filter


class GlobalFilter(Filter):
    def init(self):
        self.add_parameter(name="contrast", min=1, max=3, default=1)
        self.add_parameter(name="brightness", max=100, default=0)
        self.add_parameter(name="saturation", min=1, max=10, default=1)
        self.add_parameter(name="hue", min=0, max=179, default=0)
        self.add_parameter(name="blue", min=0, max=255, default=0)
        self.add_parameter(name="green", min=0, max=255, default=0)
        self.add_parameter(name="red", min=0, max=255, default=0)

    def compute(self, frame):
        (b, g, r) = cv.split(frame)
        b = np.clip(b + round(self.blue), 0, 255)
        g = np.clip(g + round(self.green), 0, 255)
        r = np.clip(r + round(self.red), 0, 255)
        f = cv.merge([b, g, r])

        imghsv = cv.cvtColor(f, cv.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv.split(imghsv)

        s = s * self.saturation
        h = np.mod(h + self.hue, 179)
        s = np.clip(s, 0, 255)
        imghsv = cv.merge([h, s, v])
        frame = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)

        return cv.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)
