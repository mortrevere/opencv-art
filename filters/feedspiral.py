import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
from dice import Dice

class FeedbackSpiralFilter(Filter):
    def init(self):
        self.color_osc = Oscillator(freq=12, zero=True)
        self.zoom_osc = Oscillator(freq=1)
        self.dx = random.randint(-100, 100)
        self.sx = random.randint(int(self.rows/2), int(self.rows/2))
        self.dy = random.randint(-100, 100)
        self.sy = random.randint(int(self.rows/2), int(self.rows/2))
        self.x = self.sx
        self.y = self.sy
        self.i = 0
        self.color = [255,12,86]
        self.size_osc = Oscillator(freq=14, zero=True)
        self.last_occupation = 0
        self.mode = 1
        self.new_circle()
        pass

    def new_circle(self):
        self.thickness = 2
        self.dx = random.randint(-100, 100)
        self.sx = random.randint(int(self.rows/2), int(self.rows))
        self.dy = random.randint(-100, 100)
        self.sy = random.randint(int(self.rows/2), int(self.rows))
        self.x = self.sx
        self.y = self.sy
        color = int(self.color_osc.next()*179)
        rgb = cv.cvtColor(np.uint8([[[color, 255, 255]]]), cv.COLOR_HSV2BGR)
        color = rgb[0][0]
        #self.color = (int(color[0]), int(color[1]), int(color[2]))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        

    def compute(self, frame, vid=None):
        #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image_center = tuple(np.array(frame.shape[1::-1]) / 2)
        #rot_mat = cv.getRotationMatrix2D(image_center, int(self.rot_osc.next()*3), 1.0)
        rot_mat = cv.getRotationMatrix2D(image_center, 6, 1 + self.zoom_osc.next()/100)
        #print(rot_mat)
        frame = cv.warpAffine(frame, rot_mat, frame.shape[1::-1], flags=cv.INTER_LINEAR)

        #pts1 = np.float32([[1,1],[501,8],[380,493],[501,401]])
        # Size of the Transformed Image
        #pts2 = np.float32([[0,0],[500,0],[380,500],[500,400]])
        #M = cv.getPerspectiveTransform(pts1,pts2)
        #frame = cv.warpPerspective(frame,M,frame.shape[1::-1])

        self.i += 1
        if self.i < 30:
            return self._blank
        
        bw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        non_zero = cv.countNonZero(bw)
        all_pixels = self.rows*self.cols
        occupation = non_zero/all_pixels

        int_occupation = round(occupation*10,1)
        print(int_occupation)
        if int_occupation.is_integer():
            if int_occupation != self.last_occupation:
                self.last_occupation = int_occupation
                #print("here")
                self.new_circle()
        if int_occupation - int(int_occupation) == 0.5 and int_occupation > 3:
            #self.color = (0,0,0)
            #self.thickness = 5
            pass
        #cv.circle(frame, (self.x, self.y), 16, self.color, -1)
        cv.rectangle(frame, (self.x, self.y), (self.x + self.dx, self.y + self.dy), self.color, self.thickness)

        if int_occupation > 5:
            print("here")
            cv.circle(frame, (int(self.cols/2), int(self.rows/2)), int(self.cols/2), (0,0,0), -1)
            self._previous = frame
            return frame
    
        frame = cv.addWeighted(frame,0.5,self._previous,0.5,0.0)
        self._previous = frame
        return frame
