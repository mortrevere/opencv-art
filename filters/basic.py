import numpy as np
import cv2 as cv
import math
from filter import Filter

class BasicFilter(Filter):
    def init(self):
        self.add_parameter("contrast",min=1,max=3)
        self.add_parameter("brightness",max=100)
        self.add_parameter("saturation", max=10)
        pass

    def compute(self, frame):
        imghsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv.split(imghsv)
        s = s*self.saturation
        s = np.clip(s,0,255)
        imghsv = cv.merge([h,s,v])
        frame = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)

        return cv.convertScaleAbs(frame, alpha=self.contrast, beta=self.brightness)