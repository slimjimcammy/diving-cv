from curses.ascii import alt
import time
import cv2 as cv
import yolov5
import queue

from videoInput import VideoInput
from videoOutput import VideoOutput
from cmdLineParser import CmdLineParser

def load_model():
    model = yolov5.load("best.pt")
    model.conf = 0.25  # NMS confidence threshold
    model.iou = 0.45  # NMS IoU threshold
    model.agnostic = False  # NMS class-agnostic
    model.multi_label = False  # NMS multiple labels per box
    model.max_det = 1000  # maximum number of detections per image
    return model

def process_frames(frames, model, SCORE_THRESH=0.4):
    results = model(frames)
    altered_frames = []

    for i, tensor in enumerate(results.pred):
        if tensor.numel() != 0:
            xmin, ymin, xmax, ymax, confidence, class_label = tensor[0]
            xmin = int(xmin)
            ymin = int(ymin)
            xmax= int(xmax)
            ymax = int(ymax)

            frame = cv.rectangle(frames[i], (xmin, ymin), (xmax, ymax), (0, 0, 255), 5)
            altered_frames.append(frame)
        else:
            altered_frames.append(frames[i])
        
    return altered_frames

    # altered_frames = []

    # # df = results.pandas().xyxy[0]
    df = results.pred[0][0]
    # # print(df)
    # # df = df[df.confidence > SCORE_THRESH]
    # print(df)

    # if len(df) > 0:
    #     start_point = (int(df.xmin[0]), int(df.ymin[0]))
    #     end_point = (int(df.xmax[0]), int(df.ymax[0]))
    #     frame = cv.rectangle(frame, start_point, end_point, (0, 0, 255), 5)
    #     altered_frames.append(frame)

    # return altered_frames

if __name__ == "__main__":
    model = load_model()
    print("loaded model")
    
    SCORE_THRESH = 0.4
    parser = CmdLineParser()

    file_name = parser.parse_frame_processing()

    video_input = VideoInput(file_name)
    video_input.start()

    width, height, fps, frame_count = video_input.get_info()

    output_file_name = f"{file_name}-processed.mp4"
    video_output = VideoOutput(output_file_name, width, height, fps, frame_count)
    video_output.start()
    counter = 0
    local_queue = []

    start = time.time()
    read_all_frames = False
    batch_size = 32
    counter = 1
    frame_batch = []
    while not read_all_frames and not video_output.truncated:
        try:
            frame = video_input.get_frame()
        except queue.Empty:
            read_all_frames = True
        else:
            frame_batch.append(frame)

            if len(frame_batch) >= batch_size:
                frames = process_frames(frame_batch, model, SCORE_THRESH)
                print(f"Counter: {counter}")
                counter += 1
                for f in frames:
                    video_output.enqueue_frame(f)
                frame_batch = []
            # if video_output.truncated:

    frames = process_frames(frame_batch, model, SCORE_THRESH)
    for f in frames:
        video_output.enqueue_frame(f)
    frame_batch = []

    end = time.time()
    video_input.stop()
    video_output.stop()

    print(f"Elapsed time: {end - start}")

    cv.destroyAllWindows()

