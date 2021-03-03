import numpy as np
import cv2 as cv
import math
from filter import Filter
from oscillator import Oscillator


class GradientFilter(Filter):
    def init(self):
        self.M = np.float32([[1, 0, 0], [0, 1, -3]])
        self.add_parameter("color_freq", bind="knob1", min=1 / 5, max=8, default=1)
        self.add_parameter("mouv_freq", bind="knob2", min=1, max=40, default=1)
        self.add_parameter("mouv_amplitude", bind="fader2", min=1, max=12, default=1)
        self.add_parameter("switch_lfo_mouv", bind="button2r")
        self.add_parameter("switch_thickness", bind="button2s", min=1, max=3, default=1)
        self.color_osc = Oscillator(freq=self.color_freq, zero=True)
        self.sat_osc = Oscillator(freq=self.mouv_freq, zero=True)
        self.hue_direction = 1
        pass

    def compute(self, frame):
        self.color_osc.freq = self.color_freq
        self.sat_osc.freq = self.mouv_freq
        hue = self.color_osc.next() * 179
        if self.switch_lfo_mouv:
            s = self.sat_osc.next() * self.mouv_amplitude + 3
        else:
            s = self.mouv_amplitude + 1
        self.M = np.float32([[1, 0, 0], [0, 1, round(-2 * s)]])
        imghsv = cv.cvtColor(self._blank, cv.COLOR_BGR2HSV).astype("float32")
        cv.line(
            imghsv,
            (0, self.rows),
            (self.cols, self.rows),
            (hue, 255, 255),
            round(s * self.switch_thickness),
        )
        imghsv += self._previous
        self._previous = cv.warpAffine(imghsv, self.M, (self.cols, self.rows))
        frame = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)
        return frame
