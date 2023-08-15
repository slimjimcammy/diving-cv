import queue

import cv2 as cv
from threading import Thread

class VideoInput:
    def __init__(self, source):
        self.capture = cv.VideoCapture(source)
        self.width = self.capture.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.capture.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.capture.get(cv.CAP_PROP_FPS)
        self.frame_count = self.capture.get(cv.CAP_PROP_FRAME_COUNT)

        self.frame_queue = queue.Queue()

        self.was_read, self.frame = self.capture.read()

        self.truncated = False

        self.thread = Thread(target=self.get, args=())
        self.thread.daemon = True

    def start(self):
        self.truncated = False
        self.thread.start()

    def get(self):
        while not self.truncated:
            was_read, frame = self.capture.read()
            if was_read is False:
                self.stop()
                break
            self.frame_queue.put(frame)
        self.capture.release()

    def get_info(self):
        return self.width, self.height, self.fps, self.frame_count

    def get_frame(self):
        return self.frame_queue.get(timeout=1)

    def stop(self):
        self.truncated = True