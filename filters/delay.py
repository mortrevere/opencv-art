from collections import deque
import numpy as np
import cv2 as cv
import math
from filter import Filter


class DelayFilter(Filter):
    def init(self):
        self.add_parameter("max_frames", bind="fader1", min=10, max=100, default=20)
        self.add_parameter(name="invert_dir", bind="button1r", default=True)
        self.zeros = np.zeros((self.rows, self.cols, 1), np.uint8)
        self.ones = np.ones((self.rows, self.cols, 1), np.uint8)
        self.frames = [self._blank for i in range(self.max_frames)]
        self.masks = [None for i in range(self.max_frames)]
        self.frame_count = 0

    def get_mask(self, i):
        if self.max_frames != len(self.masks):
            self.masks = [None for i in range(self.max_frames)]
        if self.masks[i] is None:
            self.masks[i] = self._get_mask(i)
        return self.masks[i]

    def _get_mask(self, i):
        return self.zeros

    def compute(self, frame):
        if self.max_frames < len(self.frames):
            self.frames = self.frames[: self.max_frames]
        elif self.max_frames > len(self.frames):
            self.frames = self.frames + [
                self._blank for i in range(len(self.frames) - self.max_frames)
            ]
        pos = self.frame_count % self.max_frames
        self.frames[pos] = frame
        res_frame = np.zeros((self.rows, self.cols, 3), np.uint8)
        for i in range(self.max_frames):
            frame_i = self.frames[(pos + self.max_frames - i) % self.max_frames]
            res_frame = cv.add(
                res_frame, cv.bitwise_and(frame_i, frame_i, mask=self.get_mask(i))
            )
        self.frame_count += 1
        return res_frame


class DelayHorizontalFilter(DelayFilter):
    def _get_mask(self, i):
        bar_size = math.ceil(self.cols / self.max_frames) + 1
        if not self.invert_dir:
            pos0 = bar_size * i
            pos1 = min(bar_size * (i + 1), self.cols)
        else:
            pos0 = max(self.cols - bar_size * (i + 1), 0)
            pos1 = max(self.cols - bar_size * i, 0)
        mask = np.zeros((self.rows, self.cols, 1), np.uint8)
        mask[:, pos0:pos1] = self.ones[:, pos0:pos1]
        return mask


class DelayVerticalFilter(DelayFilter):
    def _get_mask(self, i):
        bar_size = math.ceil(self.rows / self.max_frames) + 1
        if not self.invert_dir:
            pos0 = bar_size * i
            pos1 = min(bar_size * (i + 1), self.rows)
        else:
            pos0 = max(self.rows - bar_size * (i + 1), 0)
            pos1 = max(self.rows - bar_size * i, 0)
        mask = np.zeros((self.rows, self.cols, 1), np.uint8)
        mask[pos0:pos1, :] = self.ones[pos0:pos1, :]
        return mask


class DelayCircleFilter(DelayFilter):
    def init(self):
        super().init()
        self.center = (round(self.cols / 2.0), round(self.rows / 2.0))

    def _get_mask(self, i):
        circle_size = math.ceil(max(self.rows, self.cols) / (self.max_frames * 1.5))
        mask = np.zeros((self.rows, self.cols, 1), np.uint8)
        if self.invert_dir:
            i = self.max_frames - i - 1
        mask = cv.circle(mask, self.center, circle_size * (i + 1), 1, -1)
        return cv.circle(mask, self.center, circle_size * i, 0, -1)
