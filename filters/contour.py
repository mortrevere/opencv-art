from collections import deque
import numpy as np
import cv2 as cv
import math
from oscillator import Oscillator
from filter import Filter
import random

class ContourFilter(Filter):
    def init(self):
        self.osc = Oscillator(freq=1, zero=True)
        self.osc2 = Oscillator(freq=1/5, zero=True, phase=20)
        self.amplitude = 2
        #self.add_parameter(name="amplitude", min=10, max=60)

        self.color_osc = Oscillator(freq=1/3.09, zero=True)
        self.value_osc = Oscillator(freq=1/12, zero=True)

        self.direction = 1

        self.scale = int(self.rows/2)

    def compute(self, frame):

        color = int(self.color_osc.next()*179)
        rgb = cv.cvtColor(np.uint8([[[color, 255, 100 + int(self.value_osc.next()*155)]]]), cv.COLOR_HSV2BGR)
        color = rgb[0][0]
        color = (int(color[0]), int(color[1]), int(color[2]))

        #color = (7,0,255)


        lfo = self.osc2.next()
        self.osc.freq = lfo * 5
        o = self.osc.next()

        c = self._blank.copy()
        #color[:,:,color[:,:,1] == 0] = 255
        c[:,:,0] = color[0]
        c[:,:,1] = color[1]
        c[:,:,2] = color[2]
        #return f
        f = cv.cvtColor(cv.medianBlur(frame, 3), cv.COLOR_BGR2GRAY)
        mask = cv.adaptiveThreshold(
            f, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 5 + int(o*5)*2, 8
        )
        invert_mask = 255 - mask

        source = cv.bitwise_and(frame, c, mask=invert_mask)
        #return source
        
        #print(o, self.amplitude)
        self.M = np.float32([[1, 0, self.amplitude], [0, 1, self.amplitude]])

        if random.random() > 0.9:
            x1 = random.randint(0, self.cols)
            y1 = random.randint(0, self.cols)
            #cv.circle(source, (x1, y1), 4, (255, 255, 255), -1)

        #cv.circle(source, (int(self.cols/2 + lfo*self.scale - self.scale/2), int(self.rows/2  + o*self.scale - self.scale/2)), 1, (255,255,255), -1)

        acc = cv.addWeighted(
            self._previous,
            0.995,
            #cv.warpAffine(source, self.M, (self.cols, self.rows)),
            source,
            1,
            0.0,
        )

        if random.random() > 0.99:
            self.direction = -1*self.direction

        image_center = tuple(np.array(frame.shape[1::-1]) / 2)
        rot_mat = cv.getRotationMatrix2D(image_center, self.direction*0.1, 1.001)
        acc = cv.warpAffine(acc, rot_mat, frame.shape[1::-1], flags=cv.INTER_LINEAR)

        #acc = cv.convertScaleAbs(acc, alpha=1.1, beta=0)
        self._previous = acc
        #self._previous = cv.warpAffine(acc, self.M, (self.cols, self.rows))
        # invert_frame = cv.bitwise_not(frame)
        # acc = cv.bitwise_or(acc, cv.bitwise_and(invert_frame, invert_frame, mask=invert_mask))

        return acc
