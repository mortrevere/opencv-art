import numpy as np
import cv2 as cv
from collections import deque 
import random
import time


cap = cv.VideoCapture(2)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

i = 0
alpha = 3.0 # Simple contrast control
beta = 1    # Simple brightness control

SIZE = 30
queue = deque([None for _ in range(SIZE)])
unlock = False
_blank = None
_mask = None
previous = None
while True:
    i += 1
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    image = frame
    frame = cv.flip(frame,1)
    rows, cols, d = frame.shape

    if i == 1:
        previous = frame

    
    old = queue.pop()
    queue.appendleft(frame)

    if _blank is None:
        _blank = np.full((image.shape[0], image.shape[1]), 0, dtype=np.uint8)
        _blank = cv.cvtColor(_blank, cv.COLOR_GRAY2BGR)
    if _mask is None:
        _mask = np.full((image.shape[0], image.shape[1]), 0, dtype=np.uint8)


    total = []
    if unlock:
    
        out = _blank.copy()
        for f in queue:
            print(f)
            out += f
        #out = frame + previous
        cv.imshow('frame', out)
        #previous = out
        #time.sleep(10)

   
    if old is not None:   
        unlock = True

    #time.sleep(3)
    
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()