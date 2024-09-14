import os
import cv2
import uuid
import shutil

def to_milliseconds(seconds: float) -> int:
    return int(seconds * 1000)

def format_time(given_time: str) -> int:
    time_list = list(map(int, given_time.split(".")))
    if len(time_list) == 3:
        actual_time = (time_list[0] * 3600) + (time_list[1] * 60) + time_list[2]
    elif len(time_list) == 2:
        actual_time = (time_list[0] * 60) + time_list[1]
    else:
        actual_time = time_list[0]

    return to_milliseconds(actual_time)

def save_image(file_name, crop_frame):
    cv2.imwrite(file_name, crop_frame)

roi_list = []

def append_roi(coordinates):
    if coordinates[2] == 0 or coordinates[3] == 0:
        return
    roi_list.append(coordinates)

def select_roi(full_frame, video_name, start_time, end_time):
    if roi_list:
        for roi in roi_list:
            cv2.rectangle(full_frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 0), 2)

    cv2.namedWindow(f"{video_name}_{start_time}_{end_time}", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    coordinates = cv2.selectROI(f"{video_name}_{start_time}_{end_time}", full_frame)
    append_roi(coordinates)

def process_video():
    global roi_list

    source = input("Enter video path with video full name: ")
    fps = int(input("Enter FPS: "))
    start = input("Enter the start time of the video (Exp: 0.15): ")
    end = input("Enter the end time of the video (Exp: 3.15): ")
    out = input("Enter the output path of the video (default is 'output'): ")
    ncrop = int(input("Enter the number of maximum crops: "))
    save_type = input("Enter the output type (image, video, or both): ")

    out = out if out else "output"

    video_file = source
    video_name = os.path.split(video_file)[-1]

    video = cv2.VideoCapture(video_file)

    start_time = format_time(start) if start else 0
    end_time = format_time(end) if end else to_milliseconds(video.get(cv2.CAP_PROP_FRAME_COUNT))

    if start_time > end_time:
        raise ValueError("Start time must be less than end time")

    current_frame = 0
    sh_img = True
    video.set(cv2.CAP_PROP_POS_MSEC, start_time)
    _, frame = video.read()

    for _ in range(ncrop):
        select_roi(frame, video_name, start_time, end_time)

    cv2.destroyAllWindows()

    print(f"Selected ROIs: {len(roi_list)}")
    print(f"ROI Coordinates: {roi_list}")
    print(f"Starting extraction of '{video_name}'")

    save_directory = os.path.join(out, f"{os.path.splitext(video_name)[0]}_{start_time}_{end_time}")

    try:
        if os.path.exists(save_directory):
            shutil.rmtree(save_directory)
        os.makedirs(save_directory)

        os.chdir(save_directory)
        for i in range(len(roi_list)):
            sub_directory = f"crop_{str(i + 1)}"
            os.makedirs(sub_directory)

    except OSError as e:
        print(f"Error creating directory: {e}")

    video_writers = []
    if save_type in ["video", "both"]:
        for i, roi in enumerate(roi_list):
            crop_video_path = os.path.join(sub_directory, f"crop_{str(i + 1)}.mp4")
            video_writers.append(cv2.VideoWriter(crop_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (roi[2], roi[3])))

    while True:
        next_frame = start_time + (current_frame * (1000 / fps))
        if next_frame >= end_time:
            break

        video.set(cv2.CAP_PROP_POS_MSEC, next_frame)
        _, frame = video.read()

        if frame is not None:
            crop_index = 1
            for i, roi in enumerate(roi_list):
                if save_type in ["image", "both"]:
                    save_filename = os.path.join(sub_directory, f"crop_{crop_index}_{current_frame}_{uuid.uuid4().hex[:8]}.jpg")
                    cropped_frame = frame[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
                    save_image(save_filename, cropped_frame)
                if save_type in ["video", "both"]:
                    cropped_frame = frame[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
                    video_writers[i].write(cropped_frame)
                crop_index += 1

            current_frame += 1
        else:
            break

    if save_type in ["video", "both"]:
        for writer in video_writers:
            writer.release()

    with open("coordinates.txt", 'w') as f:
        for line in roi_list:
            f.write(f"{line}\n")

    print(f"Video extraction is finished. Total frames: {current_frame} Total person cropped: {len(roi_list)}")
    print(f"Selected ROIs: {len(roi_list)}")
    print(f"ROI Coordinates: {roi_list}")
    print(f"Extracted '{video_name}'")
    print("Video extraction completed successfully!")
    video.release()

if __name__ == "__main__":
    process_video()
