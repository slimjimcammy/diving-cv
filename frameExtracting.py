import time
import cv2 as cv
import queue
import os
import random

from videoInput import VideoInput
from videoOutput import VideoOutput
from cmdLineParser import CmdLineParser

def extract_frames(video_path, video_name, output_directory, frame_granularity):
    video_input = VideoInput(video_path)
    video_input.start()

    width, height, fps, frame_count = video_input.get_info()
    start = random.randint(0, 9)

    capture = cv.VideoCapture(video_path)
    capture.set(cv.CAP_PROP_POS_FRAMES, start)
    counter = 0
    for i in range(int(frame_count) - start):
        try:
            frame = video_input.get_frame()
            counter += 1
        except queue.Empty:
            break
        else:
            if counter % frame_granularity == 0:
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                output_file_name = f"{output_directory}/{video_name}_frame_{i + 1}.jpg"
                cv.imwrite(output_file_name, frame)
                counter = 0
    capture.release()

if __name__ == "__main__":
    parser = CmdLineParser()

    input_directory, output_directory, frame_granularity = parser.parse_frame_extracting()

    video_input = None
    video_output = None

    videos = os.listdir(input_directory)

    for video in videos:
        print(f"Beginning to process: {video}")
        video_path = os.path.join(input_directory, video)
        video_name = os.path.splitext(video)[0]

        extract_frames(video_path, video_name, output_directory, frame_granularity)
        print(f"Finished.")
        


