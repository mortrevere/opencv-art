import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
from dice import Dice

class FeedbackTriangleFilter(Filter):
    def init(self):
        self.color_osc = Oscillator(freq=1/7, zero=True)
        self.zoom_osc = Oscillator(freq=7)
        self.dx = random.randint(20, 100)
        self.sx = random.randint(int(self.rows/2), int(self.rows/2))
        self.dy = random.randint(50, 200)
        self.sy = random.randint(int(self.rows/2), int(self.rows/2))
        self.x = random.randint(int(self.rows/2), int(self.rows))
        self.y = random.randint(int(self.rows/2), int(self.rows))
        self.i = 0
        self.color = (random.randint(32, 255), random.randint(32, 255), random.randint(32, 255))
        self.size_osc = Oscillator(freq=7, zero=True)
        self.last_occupation = 0
        self.mode = 1

        self.mov_dice = Dice([1, 2, 4],p=0.5)
        self.dir_dice = Dice([-1, 1], p=1)
        self.rot_dice = Dice([20, 30, 40, 60, 90, 120], p=1)
        self.rot = 90
        self.line_osc = Oscillator(freq=1/2)
        
        #self.new_circle()
        pass
        
       

    def compute(self, frame, vid=None):
        #self.rot += self.rot_dice.next()
        #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image_center = tuple(np.array(frame.shape[1::-1]) / 1.90)
        #rot_mat = cv.getRotationMatrix2D(image_center, int(self.rot_osc.next()*3), 1.0)
        rot_mat = cv.getRotationMatrix2D(image_center, self.rot, 1 + self.zoom_osc.next()/300)
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

        avg = list(frame.mean(axis=0).mean(axis=0))
        max_val = max(avg)
        min_val = min(avg)
        #print(max_val - min_val)
        if max_val - min_val > 30:
            pass


        max_channel_index = avg.index(max_val)
        #cv.subtract(frame,(2,3,1),frame)

        if occupation > 0.23:
            tmp = self.line_osc.next()
            if tmp > 0.5:
                pos = int(tmp*(self.cols/4) + (self.cols/4))
                cv.line(frame, (pos, 0), (pos, self.rows), (0,0,0), 6)
        if occupation < 0.35:
            if self.i < 1000 or occupation < 0.15:
                cv.rectangle(frame, (self.x, self.y), (self.x + self.dx, self.y + self.dy), self.color, 2)
        else:
            frame[:,:,max_channel_index] = 0
            if random.random() < 0.2:
                self.rot = self.rot_dice.next()
        
            #frame = cv.cvtColor(imghsv.astype("uint8"), cv.COLOR_HSV2BGR)

        #color = int(self.color_osc.next()*179)
        #rgb = cv.cvtColor(np.uint8([[[color, 255, 255]]]), cv.COLOR_HSV2BGR)
        #color = rgb[0][0]
        #self.color = (int(color[0]), int(color[1]), int(color[2]))


        cv.circle(frame, (self.sx, self.sy), int(self.size_osc.next()*16) + 3, (255, 255, 255), -1)
        self.sx += self.dir_dice.next() * self.mov_dice.next()
        self.sy += self.dir_dice.next() *self.mov_dice.next()

        #b, g, r = cv.split(frame)
        #print(np.shape(r))
        #rgb = [r, g, b]
        #rgb[max_channel_index] = np.zeros((self.cols, self.rows), dtype=int)
        #r, g, b = rgb[0], rgb[1], rgb[2]
        #frame = cv.merge(rgb, 3)
        #print(avg, max_val, max_channel_index)
    
        frame = cv.addWeighted(frame,0.8,self._previous,0.2,0.0)
        #if self.i < 60:
        #    frame = cv.addWeighted(frame,0.8,self._previous,0.2,0.0)
        self._previous = frame
        return frame
