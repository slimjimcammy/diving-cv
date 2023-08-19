import time

import cv2 as cv
from threading import Thread

class VideoOutput:
    def __init__(self, file_name, width, height, fps, frame_count):
        self.frame_count = frame_count
        self.counter = 0
        self.frames_queue = []
        self.truncated = False
        print(width, height)

        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv.VideoWriter(file_name, fourcc, fps, (int(width), int(height)))

        self.thread = Thread(target=self.display, args=())
        self.thread.daemon = True

    def start(self):
        self.truncated = False
        self.thread.start()

    def display(self):
        while not self.truncated:
            if self.counter < self.frame_count:
                if self.frames_queue:
                    frame = self.frames_queue.pop(0)
                    self.video_writer.write(frame)
                    self.counter += 1
                else:
                    time.sleep(0.01)
            else:
                self.stop()
        self.video_writer.release()

    def enqueue_frame(self, frame):
        self.frames_queue.append(frame)

    def stop(self):
        self.truncated = True