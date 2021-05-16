from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random

class NoGeneratorFilter(Filter):
    def init(self):
        pass

    def compute(self, frame):
        return frame