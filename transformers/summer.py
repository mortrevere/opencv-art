from collections import deque
import numpy as np
import cv2 as cv
from filter import Filter
import random


class SummerFilter(Filter):
    def init(self):
        self.size = 9
        self._blank = np.full((self.rows, self.cols, 3), 0, dtype=np.uint8)
        self.queue = deque([self._blank.copy() for _ in range(self.size)])
        # self.queue = [self._blank.copy() for _ in range(self.size)]
        self.add_parameter("queue_len", bind="fader3", min=2, max=7, default=2)
        self.add_parameter("blur", bind="button3s")
        self.add_parameter("invert_color", bind="button3m")
        self._previous = None

    def compute(self, frame):
        queue_len = round(self.queue_len)

        if queue_len != len(self.queue):
            self.size = queue_len
            new_queue = list(self.queue)
            if queue_len > len(self.queue):
                new_queue += [
                    self._blank.copy() for _ in range(queue_len - len(self.queue))
                ]
            else:
                new_queue = new_queue[0:queue_len]
            self.queue = deque(new_queue)

        out = self._blank.copy()
        c = 0
        self.queue.pop()
        self.queue.appendleft(frame)
        for f in self.queue:
            blur_size = c % self.size + 1
            # blur_size = min(blur_size, 6)
            if self.blur:
                out += cv.blur(f, (blur_size, blur_size))
            else:
                out += f
            c += 1
        # self._previous = out
        if self.invert_color:
            return 255 - out
        else:
            return out
