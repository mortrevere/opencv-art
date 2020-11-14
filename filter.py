import numpy as np
import cv2 as cv
import math


class Parameter:
    def __init__(self, name, ref, description, min, max, default):
        self.name = name
        self.description = description
        self.min = min
        self.max = max
        self.default = default
        self.ref = ref

    def set_value(self, value):
        if value > self.max:
            value = self.max
        if value < self.min:
            value = self.min
        setattr(self.ref, self.name, value)

    def set_value_percent(self, percent):
        value = percent * (self.max - self.min) + self.min
        self.set_value(value)


class Filter:
    def __init__(self, rows, cols):
        self.parameters = {}
        self.parameters_binding = {}
        self.rows = rows
        self.cols = cols
        self._blank = np.full((self.rows, self.cols, 3), 0, dtype=np.uint8)
        self._mask = np.full((self.rows, self.cols), 0, dtype=np.uint8)
        self._previous = self._blank.copy()
        self.init()
        print(f"{self.__class__.__name__} initialized")

    @property
    def name(self):
        return self.__class__.__name__

    def add_parameter(self, name, bind=0, default=0, description="", min=0, max=1):
        setattr(self, name, default)
        self.parameters_binding[bind] = name
        self.parameters[name] = Parameter(name, self, description, min, max, default)
        print(self.parameters_binding)

    def get_parameter(self, name):
        # 'name' supports string or int to id the parameter
        # id is 0-based and follows the order of parameters declarations
        if isinstance(name, int):
            if name > len(self.parameters):
                print("Can't find parameter at index", name)
                return
            name = list(self.parameters.keys())[name]

        if isinstance(name, str):
            if not self.parameters.get(name):
                print("Can't find parameter", name)
                return
        return self.parameters[name]

    def set_parameter(self, name, value):
        self.get_parameter(name).set_value_percent(value)

    def reset_parameter(self, name):
        p = self.get_parameter(name)
        p.set_value(p.default)

    def reset_all_parameters(self):
        for name in self.parameters.keys():
            self.reset_parameter(name)
