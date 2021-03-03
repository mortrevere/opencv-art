from ui import UI
from filters import *
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
        self.input_frames = queue.Queue(maxsize=30)
        self.output_frames = queue.Queue(maxsize=10)
        self.filter_threads = []

        self.last_frame_id = 0
        self.unique = count()

        for i in range(int(config["misc"]["worker_threads"])):
            self.filter_threads += [threading.Thread(target=self.compute_worker)]
        
        self.create_ui_threads()

        self.audio = AudioCapture()
        self.create_audio_threads()

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

        for t in self.filter_threads:
            t.start()

    @property
    def current_filter_name(self):
        return self.current_filter.__class__.__name__

    @property
    def current_filter_index(self):
        return self.available_filters.index(self.current_filter_name)

    def compute_worker(self):
        while 1:
            try:
                new_frame = self.input_frames.get()
                #print(new_frame[0])
                t1 = time.time()
                self.output_frames.put(self.global_filter.compute(self.current_filter.compute(new_frame)))
                self.performance_watcher.observe(time.time() - t1)
                #time.sleep(1/30)
            except queue.Empty:
                print("empty")
                time.sleep(1/30)
            

    def compute(self, frame, vid=None):
        t1 = time.time()
        #out = self.global_filter.compute(self.current_filter.compute(frame))
        out = self.current_filter.compute(frame)#, vid=vid)
        self.performance_watcher.observe(time.time() - t1)
        return out
        #self.frame_id += 1
        #print(self.frame_id)
        try:
            self.input_frames.put(frame, block=False)
            self.last_frame = self.output_frames.get(block=(self.last_frame is None))
            return self.last_frame
        except queue.Empty:
            return self.last_frame
        except queue.Full:
            print("cleaning out input frames")
            for i in range(self.input_frames.maxsize - 1):
                self.input_frames.get()
            return self.last_frame

        try:
            self.input_frames.put((next(self.unique), frame), block=False)
            self.last_frame = self.output_frames.get(block=(self.last_frame is None))

            if self.last_frame[0] < self.last_frame_id:
                print("frames went out unordered")
            
            self.last_frame_id = self.last_frame[0]
            return self.last_frame[1]
        except queue.Empty:
            #print("empty")
            self.last_frame_id = self.last_frame[0]
            return self.last_frame[1]
        except queue.Full:
            print("cleaning out input frames")
            for i in range(self.input_frames.maxsize - 1):
                self.input_frames.get()
            self.last_frame_id = self.last_frame[0]
            return self.last_frame[1]

        if config["misc"]["enable_global_filter"]:
            return self.current_filter.compute(self.global_filter.compute(frame))
        else:
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

            self.send_ui_info(f"outq:{self.output_frames.qsize()}")
            self.send_ui_info(f"inq:{self.input_frames.qsize()}")
            time.sleep(1)
