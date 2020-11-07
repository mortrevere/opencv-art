import numpy as np
import cv2 as cv
import math

class Parameter:
    def __init__(self, name, ref, description, min, max):
        self.name = name
        self.description = description
        self.min = min
        self.max = max
        self.ref = ref
    def set_value(self, value):
        if value > self.max:
            value = self.max
        if value < self.min:
            value = self.min
        setattr(self.ref, self.name, value)
    def set_value_percent(self, percent):
        value = percent*(self.max - self.min) + self.min
        self.set_value(value)

class Filter:
    def __init__(self, rows, cols):
        self.parameters = {}
        self.rows = rows
        self.cols = cols
        self._blank = np.full((self.rows, self.cols, 3), 0, dtype=np.uint8)
        self._mask = np.full((self.rows, self.cols), 0, dtype=np.uint8)
        self._previous = self._blank.copy()
        self.init()
        print(f"{self.__class__.__name__} initialized in {self.rows}x{self.cols}")

    @property
    def name(self):
        return self.__class__.__name__

    def add_parameter(self, name, default=0, description="", min=0, max=1):
        setattr(self, name, default)
        self.parameters[name] = Parameter(name, self, description, min, max)
        print(self.parameters)

    def set_parameter(self, name, value):
        if not self.parameters.get(name):
            print("Can't find parameter", name) 
            return
        #print(name, value)
        self.parameters[name].set_value_percent(value)