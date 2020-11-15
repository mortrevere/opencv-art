from ui import UI
from filters import *

import sys, inspect
import importlib
import threading
import time
import asyncio
from config import config


class Orchestrator:
    def __init__(self, rows, cols, performance_watcher):
        self.rows = rows
        self.cols = cols
        self.performance_watcher = performance_watcher
        self.ui = UI(asyncio.get_event_loop())
        self.current_filter = None
        self.global_filter = basic.GlobalFilter(rows, cols)

        self.create_ui_threads()

        # dynamically loads filters instances
        available_filters = [module for module in sys.modules.keys() if module.startswith("filters.")]
        self.filters_module = importlib.import_module("filters")
        self.filters_module = [getattr(self.filters_module, filter[len("filters.") :]) for filter in available_filters]

        self.filters = []  # holds filters instances
        for f in self.filters_module:
            for klass in inspect.getmembers(f, inspect.isclass):
                if klass[0].endswith("Filter") and klass[0] not in (
                    "Filter",
                    "GlobalFilter",
                ):  # only load classes ending in "Filter"
                    self.filters += [klass[1](self.rows, self.cols)]  # instanciate
                    if klass[0] == config["misc"]["default_filter"]:  # default filter
                        self.current_filter = self.filters[-1]

        self.available_filters = [f.__class__.__name__ for f in self.filters]  # list of filters by name
        print(self.available_filters)

    @property
    def current_filter_name(self):
        return self.current_filter.__class__.__name__

    @property
    def current_filter_index(self):
        return self.available_filters.index(self.current_filter_name)

    def compute(self, frame):
        # return self.global_filter.compute(self.current_filter.compute(frame))
        return self.current_filter.compute(self.global_filter.compute(frame))

    def next_filter(self):
        next_i = (self.current_filter_index + 1) % (len(self.available_filters))
        self.current_filter = self.filters[next_i]

    def prev_filter(self):
        if self.current_filter_index == 0:
            next_i = len(self.available_filters) - 1
        else:
            next_i = self.current_filter_index - 1

        self.current_filter = self.filters[next_i]

    def send_ui_info(self, message):
        self.ui.send(message)

    def create_ui_threads(self):
        self.fps_thread = threading.Thread(target=self.send_fps_to_ui)
        self.fps_thread.start()

    def send_fps_to_ui(self):
        while True:
            fps = self.performance_watcher.get_fps()
            message = f"fps:{fps}"
            self.send_ui_info(message)
            time.sleep(1)
