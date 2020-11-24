import cv2 as cv
try:
    import acapture
except ImportError:
    pass

class Input:
    def __init__(self, config):
        self.config = config
        self.flip = "flip" in config \
            and config["input"]["flip"].lower() == "true"
        self.current_frame = None
        self.colorspace = None
        if "colorspace" in config["input"] and config['input']['colorspace'] != "RGB":
            try:
                self.colorspace = getattr(cv, f"COLOR_{config['input']['colorspace']}2RGB")
            except AttributeError:
                print(f"Cannot find cv.COLOR_{config['input']['colorspace']}2RGB")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get_frame(self):
        frame = self._get_frame()
        if self.colorspace is not None:
            frame = cv.cvtColor(frame, self.colorspace)
        if self.flip:
            frame = cv.flip(frame, 1)
        self.current_frame = frame
        return frame

    def _get_frame(self):
        return None

    def get_input(config):
        if config["output"]["type"] == "acapture":
            return AcaptureInput(config)
        else:
            return CV2Input(config)


class CV2Input(Input):
    def __init__(self, config):
        super().__init__(config)
        self.input_file = int(config["input"]["default_input"])
        frame = None
        while frame is None:
            self.cap = cv.VideoCapture(self.input_file)
            ret, frame = self.cap.read()
            if frame is None:
                self.input_file += 1

    def _get_frame(self):
        ret, frame = self.cap.read()
        return frame

    def __exit__(self, type, value, traceback):
        self.cap.release()


class AcaptureInput(Input):
    def __init__(self, config):
        super().__init__(config)
        self.input_file = int(config["input"]["default_input"])
        frame = None
        while frame is None:
            self.cap = acapture.open(self.input_file)
            ret, frame = self.cap.read()
            if frame is None:
                self.input_file += 1

    def _get_frame(self):
        ret, frame = self.cap.read()
        return frame

    def __exit__(self, type, value, traceback):
        self.cap.release()
