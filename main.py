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

perfs2 = PerformanceWatcher(15)
capname = "frame"
cv.namedWindow(capname, cv.WND_PROP_FULLSCREEN)
cv.setWindowProperty(capname, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
cv.moveWindow(capname, 1920, 0)
#cv.imshow(capname, frame)
while True:
    t1 = time.time()
    # cap output FPS to capture FPS
    if not stream.fresh_frame:
        #if o.output_frames.qsize() == 0:
            #print("here")
        time.sleep(1/300)
        continue
    try:
        if display:
            #_, frame_vid = stream.cap_video.read()
            #frame_vid = cv.resize(frame_vid, (720, 480))
            #cv.imshow("frame", cv.addWeighted(o.compute(stream.frame, vid=frame_vid),0.5,cv.resize(frame_vid, (720, 480)),0.7,0.0))
            #cv.imshow("frame", o.compute(stream.frame, vid=frame_vid))
            cv.imshow("frame", cv.resize(o.compute(stream.frame, vid=None), (WIDTH, HEIGHT)))
        else:
            o.compute(stream.frame)

    except Exception as e:
        print(str(e))
        pass

    if display and cv.waitKey(1) == ord("q"):
        break
    perfs2.observe(time.time() - t1)

    if i % 15 == 0:
        #print("OUT:", perfs2.get_fps())
        #print("PRC:", perfs.get_fps())
        pass
    i += 1

cv.destroyAllWindows()