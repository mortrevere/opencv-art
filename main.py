import numpy as np
import cv2 as cv
import time
from performance_watcher import PerformanceWatcher
from midi import MidiController
from orchestrator import Orchestrator
import random


def findInput():
    i = 0
    frame = None
    while frame is None:
        cap = cv.VideoCapture(i)
        ret, frame = cap.read()
        i += 1
    return cap, frame


cap, frame = findInput()

rows, cols, depth = frame.shape
# f = slit_scan_filter.SlitScanFilter(rows, cols)
# f = allpass.AllPassFilter(rows, cols)
# f = summer_filter.SummerFilter(rows, cols)
# f = foreground.ForegroundFilter(rows, cols)
# f = pixels.DragFilter(rows, cols)
# f = basic.BasicFilter(rows, cols)

perfs = PerformanceWatcher(10)

o = Orchestrator(rows, cols)
midi = MidiController(o)

while True:
    t1 = time.time()
    ret, frame = cap.read()
    rows, cols, depth = frame.shape

    frame = cv.flip(frame, 1)

    cv.imshow("frame", o.compute(frame))

    if cv.waitKey(1) == ord("q"):
        break

    # if random.randint(1,10) > 9:
    #    f.set_parameter("amplitude", random.randint(1,10)*10)

    perfs.observe(time.time() - t1)

cv.destroyAllWindows()
midiin.close_port()
