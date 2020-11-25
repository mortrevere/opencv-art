import numpy as np
import cv2 as cv
import math
from filter import Filter


class SlitScanFilter(Filter):
    def init(self):
        self.add_parameter("max_frames", bind="fader1", min=10, max=500, default=100)
        self.add_parameter(name="invert_dir", bind="button1r", default=False)
        self.ref_frame = None
        self.zeros = np.zeros((self.rows, self.cols, 1), np.uint8)
        self.ones = np.ones((self.rows, self.cols, 1), np.uint8)
        self.frame_count = 0
        self.masks = [None for i in range(self.max_frames)]

    def get_mask(self, i):
        if self.max_frames != len(self.masks):
            self.masks = [None for i in range(self.max_frames)]
        if self.masks[i] is None:
            self.masks[i] = self._get_mask(i)
        return self.masks[i]

    def _get_mask(self, i, max_frames):
        return self.zeros

    def compute(self, frame):
        mask = self.get_mask(self.frame_count % self.max_frames)
        inv_mask = 1 - mask
        maskNext = self.get_mask((self.frame_count + 1) % self.max_frames)
        if self.ref_frame is None:
            self.ref_frame = frame
        self.ref_frame = cv.bitwise_and(self.ref_frame, self.ref_frame, mask=inv_mask)
        self.ref_frame = cv.add(self.ref_frame, cv.bitwise_and(frame, frame, mask=mask))
        res_frame = cv.bitwise_and(
            self.ref_frame, self.ref_frame, mask=cv.bitwise_xor(inv_mask, maskNext)
        )
        self.frame_count += 1
        return res_frame


class SlitScanHorizontalFilter(SlitScanFilter):
    def _get_mask(self, i):
        bar_size = math.ceil(self.cols / self.max_frames) + 1
        pos0 = bar_size * i
        mask = np.zeros((self.rows, self.cols, 1), np.uint8)
        if not self.invert_dir:
            mask[:, pos0:] = self.ones[:, pos0:]
        else:
            mask[:, : self.cols - pos0] = self.ones[:, : self.cols - pos0]
        return mask


class SlitScanVerticalFilter(SlitScanFilter):
    def _get_mask(self, i):
        bar_size = math.ceil(self.rows / self.max_frames) + 1
        pos0 = bar_size * i
        mask = np.zeros((self.rows, self.cols, 1), np.uint8)
        if not self.invert_dir:
            mask[pos0:, :] = self.ones[pos0:, :]
        else:
            mask[: self.rows - pos0, :] = self.ones[: self.rows - pos0, :]
        return mask


class SlitScanCircleFilter(SlitScanFilter):
    def init(self):
        super().init()
        self.center = (round(self.cols / 2.0), round(self.rows / 2.0))

    def _get_mask(self, i):
        circle_size = math.ceil(max(self.rows, self.cols) / (self.max_frames * 2)) + 1
        if self.invert_dir:
            mask = np.zeros((self.rows, self.cols, 1), np.uint8)
            return cv.circle(
                mask, self.center, circle_size * (self.max_frames - i + 1), 1, -1
            )
        else:
            mask = np.ones((self.rows, self.cols, 1), np.uint8)
            return cv.circle(mask, self.center, circle_size * i, 0, -1)
