import numpy as np
import cv2 as cv
import time
from performance_watcher import PerformanceWatcher
from video_capture import VideoInput
from midi import MidiController
from orchestrator import Orchestrator
import random
from config import config, WIDTH, HEIGHT

perfs = PerformanceWatcher(15)
stream = VideoInput(int(config["misc"]["default_input"]))
o = Orchestrator(stream.rows, stream.cols, perfs, stream.perfs)
midi = MidiController(o)

i = 0

display = int(config["misc"]["display"]) != -1

while True:
    t1 = time.time()
    
    try:
        if display:
            cv.imshow("frame", cv.resize(o.compute(stream.frame), (WIDTH, HEIGHT)))
        else:
            o.compute(stream.frame)
    except Exception as e:
        print(str(e))
        pass

    if display and cv.waitKey(1) == ord("q"):
        break

    perfs.observe(time.time() - t1)
    if i % 15 == 0:
        print("PRC:", perfs.get_fps())
    i += 1

cv.destroyAllWindows()