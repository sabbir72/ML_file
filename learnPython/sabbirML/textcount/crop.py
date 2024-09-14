import os
import cv2
import uuid
import argparse
import shutil
import threading

def get_user_input():
    # Manually input values
    source = input("Enter the path to the video file: ")
    fps = int(input("Enter frames per second (fps): "))
    start = input("Enter the start time in seconds (format: HH.MM.SS) or leave blank for the beginning: ")
    end = input("Enter the end time in seconds (format: HH.MM.SS) or leave blank for the end: ")
    out = input("Enter the output directory for processed videos: ")
    ncrop = int(input("Enter the number of maximum crops: "))
    label = input("Enter the label for the frames: ")

    return source, fps, start, end, out, ncrop, label

# Convert seconds to milliseconds
def to_milliseconds(seconds: int) -> int:
    return seconds * 1000

# Format given time to milliseconds
def format_time(given_time) -> int:
    if not given_time:
        return 0
    time_list = str(given_time).split(".")
    time_list = [int(t) for t in time_list] if len(time_list) > 1 else [int(time_list[0])]
    if len(time_list) == 3:
        actual_time = (time_list[0] * 3600) + (time_list[1] * 60) + time_list[2]
    elif len(time_list) == 2:
        actual_time = (time_list[0] * 60) + time_list[1]
    else:
        actual_time = time_list[0]
    return to_milliseconds(actual_time)

# Save cropped frame using threading
def save_image(file_name, crop_frame):
    cv2.imwrite(file_name, crop_frame)

roi_list = []

# Append ROI to list
def append_roi(coordinates):
    if coordinates[2] == 0 and coordinates[3] == 0:
        return
    elif (coordinates[2] - coordinates[0] == 0) and (coordinates[3] - coordinates[1] == 0):
        return
    else:
        roi_list.append(coordinates)

# Select ROI
def select_roi(full_frame):
    if len(roi_list) > 0:
        for rois in roi_list:
            cv2.rectangle(full_frame, (rois[0], rois[1]), (rois[0] + rois[2], rois[1] + rois[3]), (0, 255, 0), 2)

    cv2.namedWindow(f"{video_name}_{args.start}_{args.end}", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # For Linux-based Debian OS only
    coordinates = cv2.selectROI(f"{video_name}_{args.start}_{args.end}", full_frame)
    append_roi(coordinates)

# Write frame names and labels to a text file
def write_frame_names_to_file(crop_directory, label, frame_names, frame_times):
    text_file_path = os.path.join(crop_directory, "frames.txt")
    with open(text_file_path, 'w') as file:
        for i, frame_name in enumerate(frame_names):
            file.write(f"{frame_name} Label=\"{label}\" Time=\"{frame_times[i]}\"\n")
            print(f"Added frame name: {frame_name} Label='{label}' Time='{frame_times[i]}'")

if __name__ == "__main__":
    # Get user input
    source, fps, start, end, out, ncrop, label = get_user_input()

    if source is None:
        raise ValueError("Source must be provided")

    video_file = source
    video_name = os.path.basename(video_file)

    # Read the video from specified path
    video = cv2.VideoCapture(video_file)

    # Time
    start_time = format_time(start) if start else 0
    end_time = format_time(end) if end else int(video.get(cv2.CAP_PROP_FRAME_COUNT)) * (1000 / fps)

    if start_time > end_time:
        raise ValueError("Start time must be less than end time")

    current_frame = 0
    video.set(cv2.CAP_PROP_POS_MSEC, start_time)
    frame_exist, frame = video.read()

    # Select ROI on the frame
    for i in range(ncrop):
        select_roi(frame)

    # Destroy windows once done
    cv2.destroyAllWindows()

    print(f"Selected ROIs: {len(roi_list)}")
    print(f"ROI Coordinates: {roi_list}")
    print(f"Starting extraction of '{video_name}'")

    try:
        # Creating a folder named on the video name
        save_directory = os.path.join(out, f"{os.path.splitext(video_name)[0]}_{start_time}_{end_time}")
        if os.path.exists(save_directory):
            shutil.rmtree(save_directory)
        os.makedirs(save_directory)

        os.chdir(save_directory)
        for i in range(len(roi_list)):
            sub_directory = f"crop_{i + 1}"
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)

    except OSError:
        raise NotADirectoryError("Error: Creating directory")

    cropped_frame_names = []
    frame_times = []

    while True:
        next_frame = start_time + (current_frame * (1000 / fps))
        if next_frame >= end_time:
            break

        # Reading from frame
        video.set(cv2.CAP_PROP_POS_MSEC, next_frame)
        frame_exist, frame = video.read()

        if frame_exist:
            crop_index = 1
            for roi in roi_list:
                cropped_frame = frame[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
                frame_name = f"crop_{crop_index}/crop_{crop_index}_{current_frame}_{str(uuid.uuid4())[:8]}.jpg"
                cropped_frame_names.append(frame_name)
                frame_times.append(f"{int(next_frame // 3600000):02}:{int((next_frame % 3600000) // 60000):02}:{int((next_frame % 60000) // 1000):02}.{int(next_frame % 1000):03}")  # Format: HH:MM:SS.mmm
                print(f"Saving cropped frame... {frame_name}")
                threading.Thread(target=save_image, args=(frame_name, cropped_frame), daemon=True).start()
                crop_index += 1

            current_frame += 1
        else:
            break

    # Write frame names and labels to .txt files
    for i in range(len(roi_list)):
        write_frame_names_to_file(f"crop_{i + 1}", label, cropped_frame_names, frame_times)

    with open("coordinates.txt", 'w') as f:
        for line in roi_list:
            f.write(f"{line}\n")

    # Release all space
    print(f"Video extraction is finished. Total frames: {current_frame} Total crops: {len(roi_list)}")
    print(f"Selected ROIs: {len(roi_list)}")
    print(f"ROI Coordinates: {roi_list}")
    print(f"Extracted '{video_name}'")
    video.release()
