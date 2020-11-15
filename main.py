import numpy as np
import cv2 as cv
import time
from performance_watcher import PerformanceWatcher
from midi import MidiController
from orchestrator import Orchestrator
import random
from config import config, WIDTH, HEIGHT


def findInput():
    i = int(config["misc"]["default_input"])
    frame = None
    while frame is None:
        cap = cv.VideoCapture(i)
        ret, frame = cap.read()
        i += 1
    return cap, frame


cap, frame = findInput()

rows, cols, depth = frame.shape

perfs = PerformanceWatcher(15)

o = Orchestrator(rows, cols, perfs)
midi = MidiController(o)
while True:
    t1 = time.time()
    ret, frame = cap.read()
    rows, cols, depth = frame.shape

    frame = cv.flip(frame, 1)

    try:
        # cv.imshow("frame", cv.resize(o.compute(frame), (1600, 1200)))
        cv.imshow("frame", cv.resize(o.compute(frame), (WIDTH, HEIGHT)))
    except Exception as e:
        print(str(e))
        pass

    if cv.waitKey(1) == ord("q"):
        break

    perfs.observe(time.time() - t1)
    print(perfs.get_fps())
cv.destroyAllWindows()
