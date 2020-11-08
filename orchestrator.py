from filters import *
import sys, inspect
import importlib


class Orchestrator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.current_filter = None

        # dynamically loads filters instances
        available_filters = [
            module for module in sys.modules.keys() if module.startswith("filters.")
        ]
        self.filters_module = importlib.import_module("filters")
        self.filters_module = [
            getattr(self.filters_module, filter[len("filters.") :])
            for filter in available_filters
        ]
        self.filters = []
        for f in self.filters_module:
            for klass in inspect.getmembers(f, inspect.isclass):
                if klass[0].endswith("Filter") and klass[0] != "Filter":
                    self.filters += [klass[1](self.rows, self.cols)]
                    if klass[0] == "AllPassFilter":
                        self.current_filter = self.filters[-1]

        self.available_filters = [f.__class__.__name__ for f in self.filters]
        print(self.available_filters)

    @property
    def current_filter_name(self):
        return self.current_filter.__class__.__name__

    @property
    def f(self):
        return self.current_filter

    @property
    def current_filter_index(self):
        return self.available_filters.index(self.current_filter_name)

    def compute(self, frame):
        return self.current_filter.compute(frame)

    def next_filter(self):
        next_i = (self.current_filter_index + 1) % (len(self.available_filters))
        self.current_filter = self.filters[next_i]

    def prev_filter(self):
        if self.current_filter_index == 0:
            next_i = len(self.available_filters) - 1
        else:
            next_i = self.current_filter_index - 1

        self.current_filter = self.filters[next_i]
