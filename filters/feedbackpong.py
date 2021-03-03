import numpy as np
import cv2 as cv
import math
from filter import Filter
import random
from oscillator import Oscillator
from dice import Dice

class FeedbackPongFilter(Filter):
    def init(self):
        self.dx = random.randint(4, 10)
        self.sx = random.randint(0, self.cols)
        self.dy = random.randint(4, 10)
        self.sy = random.randint(0, self.rows)
        self.x = self.sx
        self.y = self.sy
        self.i = 0
        self.color = [255,255,255]
        self.size_osc = Oscillator(freq=14, zero=True)
        self.max_size = 6
        self.last_switch = 0

        self.max_size_dice = Dice(list(range(3,32)), p=1)
        self.direction_dice = Dice([1, -1], p=1/2)

        self.rot_osc = Oscillator(freq=1, zero=True)

        self.mode = 1
        pass

    def new_direction(self):
        #print(self.max_size)
        self.dy = random.randint(-1 * self.max_size - 3, self.max_size) + 3
        self.dx = random.randint(-1 * self.max_size - 3, self.max_size) + 3
        self.max_size = self.max_size_dice.next()
        self.size_osc.freq = self.max_size_dice.next()

        #self.x = random.randint(0, self.cols)
        #self.y = random.randint(0, self.rows)
        #print(self.dx, self.dy)

    def compute(self, frame, vid=None):
        #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image_center = tuple(np.array(frame.shape[1::-1]) / 2)
        #rot_mat = cv.getRotationMatrix2D(image_center, int(self.rot_osc.next()*3), 1.0)
        rot_mat = cv.getRotationMatrix2D(image_center, 1 + self.rot_osc.next(), 1.001)
        frame = cv.warpAffine(frame, rot_mat, frame.shape[1::-1], flags=cv.INTER_LINEAR)
        self.i += 1
        if self.i < 30:
            return self._blank
        
        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x > self.cols:
            self.dx *= -1
            self.max_size = self.max_size_dice.next()
            #self.color = (random.choice([0, 255]),random.choice([0, 255]),random.choice([0, 255]))
        if self.y < 0 or self.y > self.rows:
            self.dy *= -1
            self.max_size = self.max_size_dice.next()
            #self.color = (random.choice([0, 255]),random.choice([0, 255]),random.choice([0, 255]))
        #qreturn frame
        bw = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        non_zero = cv.countNonZero(bw)
        all_pixels = self.rows*self.cols
        occupation = non_zero/all_pixels
        diff = all_pixels - non_zero

        #print(occupation)
        #print(self.x, self.y)
        #print(list(frame[self.y][self.x]))
        radius = int(self.size_osc.next() * self.max_size) + 2
        if sum(list(frame[self.y][self.x])) == 0 and occupation > 0.1 and self.mode != 0: #and self.last_switch*2 < self.i:
            #print("switch")
            self.last_switch = self.i
            self.new_direction()
            self.color = (random.choice([0, 255]),random.choice([0, 255]),random.choice([0, 255])) # if self.color[0] else (255,255,255)
        #else:
            
            #cv.circle(frame, (self.x, self.y), radius, self.color, 2)
            cv.rectangle(frame, (self.x, self.y), (self.x + radius, self.y + self.max_size), self.color, -1)

        if occupation < 0.1 or self.mode == 0:
            cv.rectangle(frame, (self.x, self.y), (self.x + radius, self.y + self.max_size), self.color, -1)

        if occupation > 0.3:
            self.color = [255,255,255]
            cv.circle(frame, (int(self.cols/2), int(self.rows/2)), int(self.cols/2), (0,0,0), -1)
            #f = self._blank.copy()
            self._previous = frame
            return frame

        frame = cv.addWeighted(frame,0.5,self._previous,0.5,0.0)
        self._previous = frame
        return frame
