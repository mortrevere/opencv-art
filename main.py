import time
from performance_watcher import PerformanceWatcher
from midi import MidiController
import keyboard
from threading import Thread
from orchestrator import Orchestrator
from config import config
from input_manager import Input
from output_manager import Output


with Input.get_input(config) as inp:
    frame = inp.get_frame()
    if frame is None:
        print("no frame received")
        exit(1)

    rows, cols, depth = frame.shape

    perfs = PerformanceWatcher(15)
    o = Orchestrator(rows, cols, perfs)
    midi = MidiController(o)

    def detect_key_press():
        keyboard.add_hotkey(config["misc"]["keyboard_next_filter"], o.next_filter)
        keyboard.add_hotkey(config["misc"]["keyboard_prev_filter"], o.prev_filter)
        keyboard.wait()

    Thread(target=detect_key_press).start()

    with Output.get_output(config) as out:
        while True:
            t1 = time.time()
            frame = inp.get_frame()
            frame = o.compute(frame)
            if not out.show(frame):
                print("quitting...")
                break

            perfs.observe(time.time() - t1)
            print(perfs.get_fps(), end="\r")

# TODO clean kill
