from ui import UI
from filters import *
from generators import *
from wipers import *
from transformers import *
from audio import AudioCapture

import sys, inspect
import importlib
import threading
import time
import asyncio
from config import config
import threading
import queue

from itertools import count

import numpy as np
import cv2 as cv

class Orchestrator:
    def __init__(self, rows, cols, performance_watcher, cap_performance_watcher):
        self.rows = rows
        self.cols = cols
        self.performance_watcher = performance_watcher
        self.cap_performance_watcher = cap_performance_watcher
        self.ui = UI(asyncio.get_event_loop())
        self.current_filter = None
        self.global_filter = basic.GlobalFilter(rows, cols)

        self.last_frame = None

        self.last_frame_id = 0
        self.unique = count()

        self.wipeout = False
        self.feedback = True
        self.feedback_wet = 0.5

        self.previous_frame = None

        self.create_ui_threads()

        self.audio = AudioCapture()
        self.create_audio_threads()

        self.engines = {"generators" : [], "wipers" : [], "transformers" : []}
        self.engines_on = {"generators" : True, "wipers" : True, "transformers" : True}
        self.engines_order = ["generators", "transformers", "wipers"]
        self.current_engine = {"generators" : 0, "wipers" : 0, "transformers" : 0}

        for engine_type in self.engines.keys():

            available = [
                module for module in sys.modules.keys() if module.startswith(engine_type + ".")
            ]

            modules = importlib.import_module(engine_type)
            modules = [
                getattr(modules, filter[len(engine_type + ".") :])
                for filter in available
            ]

            for f in modules:
                for klass in inspect.getmembers(f, inspect.isclass):
                    if klass[0].endswith("Filter") and klass[0] not in (
                        "Filter",
                        "GlobalFilter",
                    ):  # only load classes ending in "Filter"
                        self.engines[engine_type] += [klass[1](self.rows, self.cols, orchestrator=self)]  # instanciate

                        if klass[0] in ("NoWiperFilter", "SineDotFilter", "NoTransformerFilter"):
                            self.current_engine[engine_type] = len(self.engines[engine_type]) - 1
                        #if klass[0] == config["misc"]["default_filter"]:  # default filter
                        #    self.current_filter = self.filters[-1]

        # dynamically loads filters instances

        available_filters = [
            module for module in sys.modules.keys() if module.startswith("filters.")
        ]
        self.filters_module = importlib.import_module("filters")
        self.filters_module = [
            getattr(self.filters_module, filter[len("filters.") :])
            for filter in available_filters
        ]

        self.filters = []  # holds filters instances
        for f in self.filters_module:
            for klass in inspect.getmembers(f, inspect.isclass):
                if klass[0].endswith("Filter") and klass[0] not in (
                    "Filter",
                    "GlobalFilter",
                ):  # only load classes ending in "Filter"
                    self.filters += [klass[1](self.rows, self.cols, orchestrator=self)]  # instanciate
                    if klass[0] == config["misc"]["default_filter"]:  # default filter
                        self.current_filter = self.filters[-1]

        self.available_filters = [
            f.__class__.__name__ for f in self.filters
        ]  # list of filters by name
        print(self.available_filters)

        #for f in self.filters:
        #    fps = f.benchmark()
        #    if fps < 30:
        #        print("WARNING:", f.__class__.__name__, "did not pass benchmark.", round(fps,2), "fps")

    @property
    def current_filter_name(self):
        return self.current_filter.__class__.__name__


    def current_ng(self, engine_type):
        return self.engines[engine_type][self.current_engine[engine_type]]
    @property
    def current_filter_index(self):
        return self.available_filters.index(self.current_filter_name)

    def compute(self, frame, vid=None):
        t1 = time.time()
        #out = self.global_filter.compute(self.current_filter.compute(frame))
        #out = self.current_filter.compute(frame)#, vid=vid)
        #return out

        if self.wipeout:
            out = self.engines["wipers"][self.current_engine["wipers"]]._blank.copy()
            self.previous_frame = out
            self.performance_watcher.observe(time.time() - t1)
            return out

        if not self.feedback:
            frame = self.engines["wipers"][self.current_engine["wipers"]]._blank.copy()
        
        out = frame
        if self.engines_on["transformers"]:
            out = self.engines["transformers"][self.current_engine["transformers"]].compute(frame)
        if self.engines_on["generators"]:
            out = self.engines["generators"][self.current_engine["generators"]].compute(out)

    
        if self.previous_frame is not None and self.feedback:
            out = cv.addWeighted(
                self.previous_frame,
                1-self.feedback_wet,
                out,
                self.feedback_wet,
                0.0,
            )
            
        if self.engines_on["wipers"]:
            out = self.engines["wipers"][self.current_engine["wipers"]].compute(out)
        out = self.global_filter.compute(out)
        self.previous_frame = out
        #out = self.engines["generators"][0].compute(frame)
        self.performance_watcher.observe(time.time() - t1)
        return out

        #self.frame_id += 1
        #print(self.frame_id)

        if config["misc"]["enable_global_filter"]:
            return self.current_filter.compute(self.global_filter.compute(frame))
        else:
            return self.current_filter.compute(frame)

    def generator_reset(self):
        self.engines["generators"][self.current_engine["generators"]].reset()
    def next_engine(self, engine_type):
        self.current_engine[engine_type] = (self.current_engine[engine_type] + 1) % (len(self.engines[engine_type]))
        #self.current_filter = self.filters[next_i]

    def prev_engine(self, engine_type):
        if self.current_engine[engine_type] != 0:
            next_i = self.current_engine[engine_type] - 1
        else:
            next_i = len(self.engines[engine_type]) - 1

        self.current_engine[engine_type] = next_i

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

    def create_audio_threads(self):
        self.audio_thread = threading.Thread(target=self.audio.capture)
        self.audio_thread.start()

    def create_ui_threads(self):
        self.fps_thread = threading.Thread(target=self.send_fps_to_ui)
        self.fps_thread.start()

    def send_fps_to_ui(self):
        while True:
            fps = self.performance_watcher.get_fps()
            self.send_ui_info(f"fps:{fps}")

            fps = self.cap_performance_watcher.get_fps()
            self.send_ui_info(f"capfps:{fps}")

            generator_name = self.engines["generators"][self.current_engine["generators"]].__class__.__name__
            transformer_name = self.engines["transformers"][self.current_engine["transformers"]].__class__.__name__
            wiper_name = self.engines["wipers"][self.current_engine["wipers"]].__class__.__name__
            self.send_ui_info(f"engine:generator:{generator_name}")
            self.send_ui_info(f"engine:transformer:{transformer_name}")
            self.send_ui_info(f"engine:wiper:{wiper_name}")

            time.sleep(1)
