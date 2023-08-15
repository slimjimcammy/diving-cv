import cv2 as cv
import subprocess as sp
import multiprocessing as mp
import yolov5
import numpy as np
import ffmpeg
import sys
import time
import torch

def store_frames(file_name):
    cap = cv.VideoCapture(file_name)
    num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames, width, height

def process_video_chunk(frame_chunk, model, SCORE_THRESH, results_list, process):
    processed_frames = []
    for i, frame in enumerate(frame_chunk):
        # print(f"Process #{process + 1}: {i + 1}")
        processed_frame = process_frame(frame, model, SCORE_THRESH)
        # output_frames.put(processed_frame)
        processed_frames.append(processed_frame)
    print("Post-loop")
    results_list.extend(processed_frames)
    return results_list

def process_frame(frame, model, SCORE_THRESH):
    # frame_resized = cv.resize(frame, (height, width))
    # frame_tensor = torch.from_numpy(frame_resized.transpose(2, 0, 1)).float().unsqueeze(0) / 255.0
    # # print(frame_tensor.shape)

    results = model(frame)
    df = results.pandas().xyxy[0]
    df = df[df.confidence > SCORE_THRESH]

    if len(df) > 0:
        start_point = (int(df.xmin[0]), int(df.ymin[0]))
        end_point = (int(df.xmax[0]), int(df.ymax[0]))
        frame = cv.rectangle(frame, start_point, end_point, (0, 0, 255), 5)

    return frame

if __name__ == "__main__":
    file_name = ""
    if len(sys.argv) != 2:
        print("Usage: python3 videoParser.py [video file name]")
        exit()
    else:
        file_name = sys.argv[1]

    results_list = mp.Manager().list()
    model = yolov5.load("best.pt")
    # model_dict = torch.load('best.pt')
    # print(model_dict.keys())
    # torch.save(model_dict, "best.pt")
    # model = model_dict["model"]
    # model.float()
    model.conf = 0.25  # NMS confidence threshold
    model.iou = 0.45  # NMS IoU threshold
    model.agnostic = False  # NMS class-agnostic
    model.multi_label = False  # NMS multiple labels per box
    model.max_det = 1000  # maximum number of detections per image

    SCORE_THRESH = 0.4

    video_frames, width, height = store_frames(file_name)
    # num_processes = mp.cpu_count() - 2
    num_processes = 1

    frame_chunks = np.array_split(video_frames, num_processes)
    print(f"Num chunks: {len(frame_chunks)}")

    processes = [
        mp.Process(
            target=process_video_chunk, 
            args=[frame_chunks[i], model, 
                  SCORE_THRESH, results_list, i]) 
                for i in range(num_processes)
        ]
    
    start = time.time()
    for process in processes:
        process.start()

    for process in processes:
        process.join()
    end = time.time()

    print(f"Elapsed: {end - start}")
    print("After processes finished")

    i = 0
    while i < len(results_list):
        cv.imshow("video", results_list[i])

        if cv.waitKey(25) & 0xFF == ord('q'):
            break

        time.sleep(0.05)
        i += 1

    cv.destroyAllWindows()
