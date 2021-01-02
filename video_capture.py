import threading
import cv2 as cv
import time
from performance_watcher import PerformanceWatcher

OPTIONS = {"CAP_PROP_FRAME_WIDTH": 720, "CAP_PROP_FRAME_HEIGHT": 480, "CAP_PROP_FOURCC": cv.VideoWriter_fourcc(*'YUYV')}
capture_properties = ['CAP_PROP_POS_MSEC', 'CAP_PROP_POS_FRAMES', 'CAP_PROP_POS_AVI_RATIO', 'CAP_PROP_FRAME_WIDTH', 'CAP_PROP_FRAME_HEIGHT', 'CAP_PROP_FPS', 'CAP_PROP_FOURCC', 'CAP_PROP_FRAME_COUNT', 'CAP_PROP_FORMAT', 'CAP_PROP_MODE', 'CAP_PROP_BRIGHTNESS', 'CAP_PROP_CONTRAST', 'CAP_PROP_SATURATION', 'CAP_PROP_HUE', 'CAP_PROP_GAIN', 'CAP_PROP_EXPOSURE', 'CAP_PROP_CONVERT_RGB', 'CAP_PROP_WHITE_BALANCE_BLUE_U', 'CAP_PROP_RECTIFICATION', 'CAP_PROP_MONOCHROME', 'CAP_PROP_SHARPNESS', 'CAP_PROP_AUTO_EXPOSURE', 'CAP_PROP_GAMMA', 'CAP_PROP_TEMPERATURE', 'CAP_PROP_TRIGGER', 'CAP_PROP_TRIGGER_DELAY', 'CAP_PROP_WHITE_BALANCE_RED_V', 'CAP_PROP_ZOOM', 'CAP_PROP_FOCUS', 'CAP_PROP_GUID', 'CAP_PROP_ISO_SPEED', 'CAP_PROP_BACKLIGHT', 'CAP_PROP_PAN', 'CAP_PROP_TILT', 'CAP_PROP_ROLL', 'CAP_PROP_IRIS',     'CAP_PROP_SETTINGS', 'CAP_PROP_BUFFERSIZE', 'CAP_PROP_AUTOFOCUS']


class VideoInput:
    def __init__(self, default_input):
        self.default_input = default_input
        # start the thread to read frames from the video stream
        self.perfs = PerformanceWatcher(15)
        self.cap, self.frame = self.findInput()
        self.rows, self.cols, self.depth = self.frame.shape
        #self.capture_thread = threading.Thread(target=self.update)
        #self.capture_thread.start()
        threading.Thread(target=self.update).start()
        for i in range(38):
            print (i, capture_properties[i], self.cap.get(i))

    def findInput(self):
        i = self.default_input
        print(i)
        frame = None
        while frame is None:
            cap = cv.VideoCapture(i, cv.CAP_V4L2)
            for o, v in OPTIONS.items():
                print(getattr(cv, o), o, v)
                cap.set(getattr(cv, o), v)
            ret, frame = cap.read()
            i += 1
        return cap, frame

    def update(self):
        i = 0
        while 1:
            t1 = time.time()
            ret, self.frame = self.cap.read()
            self.perfs.observe(time.time() - t1)
            if i % 15 == 0:
                print("CAP:", self.perfs.get_fps())
            i += 1
