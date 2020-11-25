import cv2 as cv
import numpy as np
from threading import Thread
try:
    import pyvirtualcam
except ImportError:
    pass
try:
    import virtualvideo
except ImportError:
    pass


def resize_image(img0, w2, h2):
    h0, w0, c = img0.shape[:3]
    h1 = (w0 * h2) // w2
    if h1 < h0:
        x_pos = 0
        y_pos = abs(h1 - h0) // 2
        w1 = w0
    else:
        w1 = (h0 * w2) // h2
        x_pos = abs(w1 - w0) // 2
        y_pos = 0
        h1 = h0
    img1 = img0[y_pos:h0-y_pos, x_pos:w0-x_pos, :]
    return cv.resize(img1, (w2, h2), cv.INTER_AREA)


class Output:
    def __init__(self, config):
        self.config = config
        self.width = int(config["output"]["width"])
        self.height = int(config["output"]["height"])
        self.colorspace = None
        if "colorspace" in config["input"] and config['input']['colorspace'] != "RGB":
            try:
                self.colorspace = getattr(cv, f"COLOR_RGB2{config['input']['colorspace']}")
            except AttributeError:
                print(f"Cannot find cv.COLOR_RGB2{config['input']['colorspace']}")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def show(self, frame):
        frame = resize_image(frame, self.width, self.height)
        if self.colorspace is not None:
            frame = cv.cvtColor(frame, self.colorspace)
        return self._show(frame)

    def _show(self, frame):
        return False

    def get_output(config):
        if config["output"]["type"] == "pyvirtualcam":
            return PyVirtualCamOutput(config)
        elif config["output"]["type"] == "v4l2":
            return V4L2Output(config)
        else:
            return CV2Output(config)


class CV2Output(Output):
    def __init__(self, config):
        super().__init__(config)
        self.fullscreen = "fullscreen" in config["output"] \
            and config["output"]["fullscreen"].lower() == "true"
        self.title = "Q to quit"
        if self.fullscreen:
            cv.namedWindow(self.title, cv.WND_PROP_FULLSCREEN)
            cv.setWindowProperty(self.title, cv.WND_PROP_FULLSCREEN, 1)

    def __exit__(self, type, value, traceback):
        cv.destroyAllWindows()

    def _show(self, frame):
        cv.imshow(self.title, frame)
        return cv.waitKey(1) != ord("q")


class PyVirtualCamOutput(Output):
    def __init__(self, config):
        super().__init__(config)
        if "fps" in config["output"]:
            self.fps = int(config["output"]["fps"])
        else:
            self.fps = 30

    def __enter__(self):
        self.cam = pyvirtualcam.Camera(width=self.width,
                                       height=self.height,
                                       fps=self.fps)
        self.cam.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.cam.__exit__(type, value, traceback)

    def _show(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_RGB2RGBA)
        self.cam.send(frame)
        self.cam.sleep_until_next_frame()
        return False


class V4L2Output(Output):
    """
    see https://github.com/umlaeute/v4l2loopback
    and https://github.com/Flashs/virtualvideo
    """

    def __init__(self, config):
        super().__init__(config)
        self.output_file = int(config["output"]["output_file"])
        if "fps" in config["output"]:
            self.fps = int(config["output"]["fps"])
        else:
            self.fps = 30

        class MyVideoSource(virtualvideo.VideoSource):
            def __init__(self, width, height, fps):
                self._fps = fps
                self._size = (width, height)
                self.running = True
                self.frame = np.zeros((height, width, 3), np.uint8)

            def img_size(self):
                return self._size

            def fps(self):
                return self._fps

            def generator(self):
                while self.running:
                    yield self.frame

        self.vidsrc = MyVideoSource(self.width, self.height, self.fps)
        self.fvd = virtualvideo.FakeVideoDevice()
        self.fvd.init_input(self.vidsrc)
        self.fvd.init_output(self.output_file, self.width, self.height, fps=self.fps)

    def __enter__(self):
        Thread(target=self.fvd.run).start()
        return self

    def __exit__(self, type, value, traceback):
        self.vidsrc.running = False

    def _show(self, frame):
        self.vidsrc.frame = frame
        return True
