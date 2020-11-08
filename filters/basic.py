import numpy as np
import cv2 as cv
import math
from filter import Filter


class GlobalFilter(Filter):
    def init(self):
        self.add_parameter(name="contrast", min=1, max=3, default=1)
        self.add_parameter(name="brightness", max=100, default=0)
        self.add_parameter(name="saturation", min=1, max=10, default=1)

    def compute(self, frame):
        imghsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv.split(imghsv)
        s = s * self.saturation
        s = np.clip(s, 0, 255)
        imghsv = cv.merge([h, s, v])
        frame = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)

        return cv.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)
