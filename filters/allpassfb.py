import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator

class AllPassFilterFB(Filter):
    def init(self):
        self.uy = int(480/4)
        self.y = 0
        self.h = self.uy*2 + 40
        self.ux = int(720/4)
        self.x = 120
        self.w = self.ux*4 - (2*self.x)
        print(self.cols, self.rows)
        self.prev = None
        self.i = 0
        self.flip = 1
        self.m = Oscillator(1.618, zero=True)
        self.o = Oscillator(1/16, zero=True)
        self.c = Oscillator(0.1, zero=True)
        self.o2 = Oscillator(1/9, zero=True)
        self.M = np.float32([[1, 0, random.choice([2, -2, 0])], [0, 1, 0]])
        pass

    def compute(self, frame):
        #print(self.o.next()*self.rows)
        #return frame#cv.resize(frame,(1080, 1920), interpolation = cv.INTER_CUBIC)

        


        mod = self.m.next()
        self.o2.freq = mod*mod/4
        #self.o.freq = mod

        pos = int(self.o.next()*self.cols)
        pos2 = int(self.o2.next()*self.rows)
        color = int(self.c.next()*179)
        #print(color)
        rgb = cv.cvtColor(np.uint8([[[color, 255, 255]]]), cv.COLOR_HSV2BGR)
        color1 = rgb[0][0]
        #print((color[0], color[1], color[2]))
        #cv.line(frame,(pos,0),(pos,self.rows),(int(color1[0]), int(color1[1]), int(color1[2])),int(mod*mod*14)*0 + 10)

        
        test = self.i%30
        if test == 0:
            self.d = random.randint(0,self.rows)
            self.p = random.randint(0,self.cols)  
            self.coord = (self.d + random.randint(0,self.rows-self.d), self.p + random.randint(0,self.cols-self.p))
        if self.i%87 < 4:
            pass
            #print("here", d, p)
            #cv.rectangle(frame, (self.d, self.p), self.coord, (int(color1[0]), int(color1[1]), int(color1[2])), -1)

        rgb = cv.cvtColor(np.uint8([[[179-color, 255, color + (255-179)]]]), cv.COLOR_HSV2BGR)
        color2 = rgb[0][0]

        
        #cv.line(frame,(0,pos2),(self.cols,pos2),(int(color2[0]), int(color2[1]), int(color2[2])),int(mod*7)*0 + 2)
        #cv.line(frame,(0,pos2),(self.cols,pos2),(int(color2[0]), 0, 0),int(mod*7)*0 + 2)
        cv.circle(frame,(pos,pos2), int(mod*5) + 2, (255, 255, 255), -1)

        #cv.circle(frame,(pos,pos2), int(mod*6) + 3, (int(color2[0]), int(color2[1]), int(color2[2])), -1)

        #oframe = frame
        #f = frame
        #if random.random() > 0.63:
        #    f = cv.cvtColor(cv.medianBlur(frame, 3), cv.COLOR_BGR2GRAY)
        #    mask = cv.adaptiveThreshold(
        #        f, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 17, 4
        #    )
        #    invert_mask = 255 - mask

        #    f = cv.bitwise_and(frame, frame, mask=invert_mask)
        #frame = cv.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
        #f = f[self.y:self.y+self.h, self.x:self.x+self.w]
        #if self.prev is not None:
            #f = cv.bitwise_xor(self.prev, f)  
            #f += self.prev
        #    f = cv.addWeighted(
        #    self.prev,
        #    0.5,
        #    f,
        #    0.5,
        #    0.0,

        self.i += 1
        #if self.i % 100 == 0:
            #self.flip = -1*self.flip
            #frame = cv.flip(frame, 0)
            
        #)
        #cv.line(img,(0,0),(511,511),(255,0,0),5)
       
        if False:
            imghsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV).astype("float32")
            (h, s, v) = cv.split(imghsv)

            s = s * (0.9 + mod/3)
            h = np.mod(h + 4, 179)
            s = np.clip(s, 0, 255)
            imghsv = cv.merge([h, s, v])
            frame = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)
        #if mod < 0.1:
        if self.i%137 < 10 and self.i > 120:
            pass
            
            frame[np.where((frame==[255,255,255]).all(axis=2))] = [0,0,0]
            frame[np.where((frame==[255,0,0]).all(axis=2))] = [0,0,0]
            frame[np.where((frame==[0,255,0]).all(axis=2))] = [0,0,0]
            frame[np.where((frame==[0,0,255]).all(axis=2))] = [0,0,0]
            #frame = 255 - frame
            self.prev = frame
            return frame

            #frame = 255 - frame
        #self.prev = cv.blur(f, (3, 3))
        #frame = cv.resize(f,(self.cols, self.rows), interpolation = cv.INTER_CUBIC)
        #frame = cv.resize(frame,(1080, 1920), interpolation = cv.INTER_CUBIC)

        
        #f = cv.bitwise_xor(f, self._previous)
        if self.i < 120:
            return self._blank

        if self.i%120 == 0:
            #self.M = np.float32([[1, 0, random.choice([2, -2, 0])], [0, 1, random.choice([1, -1, 0])]])
            self.M = np.float32([[1, 0, 0], [0, 1, random.choice([1, -2, 0])]])
        frame = cv.warpAffine(frame, self.M, (self.cols, self.rows))


        if self.prev is not None:
            #f = cv.bitwise_xor(self.prev, f)  
            pass
            frame = cv.addWeighted(self.prev,0.5,frame,0.5,0.0)
            
        self.prev = frame
       
        return frame
