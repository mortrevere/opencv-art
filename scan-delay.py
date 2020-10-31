import numpy as np
import cv2 as cv
from collections import deque 
import random
cap = cv.VideoCapture(2)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 800)

i = 0

SIZE = 30
queue = deque([None for _ in range(SIZE)])
unlock = False
_blank = None
_mask = None

while True:
    i += 1
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    image = frame
    frame = cv.flip(frame,1)
    rows, cols, d = frame.shape
    
    old = queue.pop()
    queue.appendleft(frame)

    if _blank is None:
        _blank = np.full((image.shape[0], image.shape[1]), 0, dtype=np.uint8)
        _blank = cv.cvtColor(_blank, cv.COLOR_GRAY2BGR)
    if _mask is None:
        _mask = np.full((image.shape[0], image.shape[1]), 0, dtype=np.uint8)


    total = []
    if unlock:
        blank = _blank.copy()
        c = 0
        for f in queue:
            mask = _mask.copy()
            pos = round(c*600/SIZE)
            w = round(600/SIZE)

            cv.line(mask,(0,pos),(800,pos),(255,255,255),w-1)
            stripe = cv.bitwise_and(f,f,mask=mask)
            blank = cv.bitwise_or(stripe, blank)
            c += 1
        cv.imshow('frame', blank)


   
    if old is not None:   
        unlock = True
    
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()