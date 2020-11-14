import numpy as np
import cv2 as cv
import math
import random
from filter import Filter


class ForegroundFilter(Filter):
    def init(self, size=50):
        self.size = size
        self._blank = np.full((self.rows, self.cols, 3), 0, dtype=np.uint8)
        self._mask = np.full((self.rows, self.cols), 0, dtype=np.uint8)
        self.queue = [self._blank.copy() for _ in range(self.size)]
        self.frame_counter = 0
        self.previous = None
        self.M = np.float32([[1, 0, 5], [0, 1, 5]])

        self.current_walk = {}

    def smooth_random(self, id, min=1, max=5, deviation=5):
        if not self.current_walk.get(id):
            self.current_walk[id] = 0
        direction = random.randint(-1, 1)
        if direction == 0:
            return 0
        speed = random.randint(0, deviation)
        if direction < 0:
            self.current_walk[id] -= speed
        if direction > 0:
            self.current_walk[id] += speed

        if self.current_walk[id] < min:
            self.current_walk[id] = min
        if self.current_walk[id] > max:
            self.current_walk[id] = max
        return self.current_walk[id]

    def compute(self, frame):
        # out = self._blank.copy()
        f = cv.cvtColor(cv.medianBlur(frame, 3), cv.COLOR_BGR2GRAY)
        mask = cv.adaptiveThreshold(f, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 17, 4)
        invert_mask = 255 - mask

        og_frame = frame.copy()

        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv.split(frame)
        s = s * 1.2
        s = np.clip(s, 0, 255)
        frame = cv.merge([h, s, v])
        frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR).astype("uint8")

        f = cv.bitwise_and(frame, frame, mask=invert_mask)
        # return cv.medianBlur(f,3)
        if self.previous is not None:
            f = cv.bitwise_xor(self.previous, f)

        speed = self.smooth_random("speed", -30, 30, 1)
        direction1 = self.smooth_random("direction1", 0, 1, 1)
        direction2 = self.smooth_random("direction2", 0, 1, 1)
        direction3 = self.smooth_random("direction3", 0, 1, 1)
        direction4 = self.smooth_random("direction4", 0, 1, 1)
        # print(speed, direction1, direction2, direction3, direction4)
        # self.M = np.float32([[1,0,speed],[0,1,speed]])
        # self.M = np.float32([[direction1,1-direction1,speed],[direction3,1-direction3,speed]])
        self.M = np.float32([[direction1, 1 - direction1, speed], [direction3, 1 - direction3, speed]])
        f = cv.warpAffine(f, self.M, (self.cols, self.rows))

        self.previous = cv.cvtColor(cv.warpAffine(invert_mask, self.M, (self.cols, self.rows)), cv.COLOR_GRAY2BGR,)
        self.previous = cv.bitwise_or(f, self.previous)
        # f = cv.bitwise_or(cv.cvtColor(invert_mask, cv.COLOR_GRAY2BGR), f)
        f = cv.bitwise_or(f, og_frame)

        # f = cv.bitwise_and(f,frame,mask=mask)

        return f
