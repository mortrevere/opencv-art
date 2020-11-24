import cv2 as cv
try:
    import pyvirtualcam
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

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def show(self, frame):
        frame = resize_image(frame, self.width, self.height)
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
    def __exit__(self, type, value, traceback):
        cv.destroyAllWindows()

    def _show(self, frame):
        cv.imshow("Q to quit", frame)
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
    pass  # TODO
