import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
from dice import Dice

class AudioFilter(Filter):
    def init(self):
        self.color_osc = Oscillator(freq=0.123, zero=True)
        self.value_osc = Oscillator(freq=1/12, zero=True)
        self.width_osc = Oscillator(freq=1, zero=True)

        self.attacker_osc = Oscillator(freq=1.76, phase=12, zero=True)
        self.attacker_coords = None

        self.half_width = int(self.cols/2)
        self.half_height = int(self.rows/2)

        self.quarter_height = int(self.rows/4)
        self.quarter_width = int(self.cols/4)

        self.wiggle = Dice([-1, 1], p=1/500)

        self.i = 0

        self.mode = 0
        self.circle_size = 0
        self.line_size = 0

        self.last_center = (self.half_width,self.half_height)

        self.n = 2
        self.czs = [1]*self.n

        pass

    def compute(self, frame, vid=None):
        self.i += 1
        if self.i < 15:
            return self._blank

        image_center = tuple(np.array(frame.shape[1::-1]) / 1.90)
        #rot_mat = cv.getRotationMatrix2D(image_center, int(self.rot_osc.next()*3), 1.0)
        if self.o.audio.peaking():
            if random.random() > 0.01:
                rot_mat = cv.getRotationMatrix2D(image_center, random.choice([1,-1]), 1.04)
            else:
                rot_mat = cv.getRotationMatrix2D(image_center, random.choice([90,-90]), 1.04)
                frame = 255 - frame
            frame = cv.flip(frame, -1)
        else:
            rot_mat = cv.getRotationMatrix2D(image_center, 0, 1.02)
        #print(rot_mat)
        frame = cv.warpAffine(frame, rot_mat, frame.shape[1::-1], flags=cv.INTER_LINEAR)

        #color = min(round(self.o.audio.intensity * 179),179)
        color = int(self.color_osc.next()*179)
        rgb = cv.cvtColor(np.uint8([[[color, 255, 100 + int(self.value_osc.next()*155)]]]), cv.COLOR_HSV2BGR)
        color = rgb[0][0]
        color = (int(color[0]), int(color[1]), int(color[2]))


        #print(self.o.audio.intensity)
        
        next_line_size = round(self.o.audio.intensity * self.half_width/8 + 1)
        if next_line_size > self.line_size:
            self.line_size = next_line_size
        if self.line_size > 20:
            self.line_size -= 1
        
        cv.line(frame,(self.half_width,0),(self.half_width,self.rows),color,self.line_size)
        next_circle_size = round(self.o.audio.intensity * self.half_width/8 + 1)
        self.circle_size = next_circle_size
        if self.o.audio.peaking():
            
            if next_circle_size/2 > self.circle_size:
                self.circle_size = next_circle_size
            print("peaking")

            #imghsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV).astype("float32")
            #(h, s, v) = cv.split(imghsv)

            #v = v * 0.5#self.saturation
            #h = np.mod(h + 10, 179)
            #v = np.clip(v, 0, 255)
            #imghsv = cv.merge([h, s, v])
            #frame = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)
            #self._previous = frame
            #return frame


        if self.circle_size > 5:
            self.circle_size -= 2
        else:
            self.circle_size = round(self.o.audio.intensity * self.half_width/8 + 1)
                    #print(self.circle_size)
        #cv.square(frame,(self.half_width,self.half_height),self.circle_size,(0,0,0),-1)
        #cv.rectangle(frame,(0,self.half_height),(self.cols,self.half_height),(0,0,0),self.circle_size)
        center = (self.half_width,self.half_height)

        self.czs[self.i%self.n] = self.circle_size


        for i in range(self.n):
            #cz = round(self.czs[i]/2)
            cz = self.czs[i]
            grey = 0#round(i*100/self.n)
            cv.rectangle(frame,(center[0]-cz,center[1]-cz),(center[0]+cz,center[1]+cz),(grey,grey,grey), -1)
        #cv.rectangle(frame,(center[0]-self.circle_size,center[1]-self.circle_size),(center[0]+self.circle_size,center[1]+self.circle_size),(0,0,0), -1)
        
        #center = self.last_center
        #cv.rectangle(frame,(center[0]-self.circle_size,center[1]-self.circle_size),(center[0]+self.circle_size,center[1]+self.circle_size),(0,0,0), -1)
        #self.last_center = center

        if self._previous is not None:
            frame = cv.addWeighted(frame,0.5,self._previous,0.5,0.0)

        #frame = cv.blur(frame,(3,3))
        self._previous = frame
        return frame
