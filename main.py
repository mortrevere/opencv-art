import numpy as np
import cv2 as cv
import time
from performance_watcher import PerformanceWatcher
from filters import *

cap = cv.VideoCapture(0)
ret, frame = cap.read()
rows, cols, depth = frame.shape

sfilter = slit_scan_filter.SlitScanFilter(rows, cols, 40)
perfs = PerformanceWatcher(10)

while True:
    t1 = time.time()
    ret, frame = cap.read()
    rows, cols, depth = frame.shape

    cv.imshow('frame', sfilter.compute(frame))
   
    if cv.waitKey(1) == ord('q'):
        break

    perfs.observe(time.time() - t1)

    print(command, perfs.get_fps())

cv.destroyAllWindows()