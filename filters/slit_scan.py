import numpy as np
import cv2 as cv
import math
from filter import Filter


class DelayFilter(Filter):
    def init(self, masks):
        self.max_frames = len(masks)
        self.frames = [np.zeros((self.rows, self.cols, 3), np.uint8)] * len(masks)
        self.masks = masks
        self.frame_count = 0

    def compute(self, frame):
        pos = self.frame_count % self.max_frames
        self.frames[pos] = frame
        res_frame = np.zeros((self.rows, self.cols, 3), np.uint8)
        for i in range(self.max_frames):
            frame_i = self.frames[(pos + self.max_frames - i) % self.max_frames]
            res_frame = cv.add(res_frame, cv.bitwise_and(frame_i, frame_i, mask=self.masks[i]))
        self.frame_count += 1
        return res_frame


class SlitScanLeftRightFilter(DelayFilter):
    def init(self):
        max_frames = 50
        bar_size = math.ceil(self.cols / max_frames) + 1
        masks = [cv.rectangle(
            np.zeros((self.rows, self.cols, 1), np.uint8),
            (bar_size * i, 0),
            (bar_size * (i + 1) - 1, self.rows), 1, -1)
                for i in range(max_frames)]
        super().init(masks)


class SlitScanRightLeftFilter(DelayFilter):
    def init(self):
        max_frames = 50
        bar_size = math.ceil(self.cols / max_frames) + 1
        masks = [cv.rectangle(
            np.zeros((self.rows, self.cols, 1), np.uint8),
            (bar_size * i, 0),
            (bar_size * (i + 1) - 1, self.rows), 1, -1)
                for i in range(max_frames - 1, -1, -1)]
        super().init(masks)


class SlitScanUpDownFilter(DelayFilter):
    def init(self):
        max_frames = 50
        bar_size = math.ceil(self.rows / max_frames) + 1
        masks = [cv.rectangle(
            np.zeros((self.rows, self.cols, 1), np.uint8),
            (0, bar_size * i),
            (self.cols, bar_size * (i + 1) - 1), 1, -1)
                for i in range(max_frames)]
        super().init(masks)

class SlitScanDownUpFilter(DelayFilter):
    def init(self):
        max_frames = 50
        bar_size = math.ceil(self.rows / max_frames) + 1
        masks = [cv.rectangle(
            np.zeros((self.rows, self.cols, 1), np.uint8),
            (0, bar_size * i),
            (self.cols, bar_size * (i + 1) - 1), 1, -1)
                for i in range(max_frames - 1, -1, -1)]
        super().init(masks)

class SlitScanCircleOutFilter(DelayFilter):
    def init(self):
        max_frames = 50
        circle_size = math.ceil(max(self.rows, self.cols) / max_frames) + 1
        masks = []
        center = (round(self.cols/2.0), round(self.rows/2.0))
        for i in range(max_frames):
            mask = np.zeros((self.rows, self.cols, 1), np.uint8)
            mask = cv.circle(mask, center, circle_size * (i + 1), 1, -1)
            mask = cv.circle(mask, center, circle_size * i, 0, -1)
            masks += [mask]
        super().init(masks)

class SlitScanCircleInFilter(DelayFilter):
    def init(self):
        max_frames = 50
        circle_size = math.ceil(max(self.rows, self.cols) / max_frames) + 1
        masks = []
        center = (round(self.cols/2.0), round(self.rows/2.0))
        for i in range(max_frames - 1, -1, -1):
            mask = np.zeros((self.rows, self.cols, 1), np.uint8)
            mask = cv.circle(mask, center, circle_size * (i + 1), 1, -1)
            mask = cv.circle(mask, center, circle_size * i, 0, -1)
            masks += [mask]
        super().init(masks)
