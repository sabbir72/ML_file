import os
import cv2
import uuid
import argparse
import shutil
import threading

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default=None, help="Directory of saved videos")
    parser.add_argument("--fps", type=int, default=5, help="Frame per second")
    parser.add_argument("--start", type=str, default=None, help="Start time of the video. Exp: 3.15")
    parser.add_argument("--end", type=str, default=None, help="End time of the video")
    parser.add_argument("--out", type=str, default="output", help="output path of the video")
    parser.add_argument("--ncrop", type=int, default=10, help="No of Max crops ")

    return parser.parse_args()


# convert seconds to milliseconds
def to_milliseconds(seconds: int) -> int:
    return seconds * 1000


# format given time to seconds
def format_time(given_time) -> int:
    time_list = str(given_time).split(".")
    time_list = [int(t) for t in time_list] if len(time_list) > 1 else [int(time_list[0])]
    if len(time_list) == 3:
        actual_time = (time_list[0] * 60 * 60) + (time_list[1] * 60) + time_list[2]
    elif len(time_list) == 2:
        actual_time = (time_list[0] * 60) + time_list[1]
    else:
        actual_time = time_list[0]

    return to_milliseconds(actual_time)


# frame write from threading
def save_image(file_name, crop_frame):
    cv2.imwrite(file_name, crop_frame)


roi_list = []
# input of ROI which should not be accepted
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

    cv2.namedWindow(f"{video_name}_{args.start}_{args.end}", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  ## for linux-based Debian OS only. Comment this line on Widnows 10 or later
    coordinates = cv2.selectROI(f"{video_name}_{args.start}_{args.end}", frame)
    append_roi(coordinates)


if __name__ == "__main__":
    args = get_parser()

    if args.source is None:
        raise ValueError("Source must be provided")

    video_file = args.source
    video_name = video_file.split("/")[-1]

    # Read the video from specified path
    video = cv2.VideoCapture(video_file)


    # time
    start_time = format_time(args.start) if args.start is not None else 0
    end_time = format_time(args.end) if args.end is not None else to_milliseconds(video.get(cv2.CAP_PROP_FRAME_COUNT))

    if start_time > end_time:
        raise ValueError("Start time must be less than end time")

    current_frame = 0
    sh_img = True
    video.set(cv2.CAP_PROP_POS_MSEC, start_time)
    frame_exist, frame = video.read()

    #Select ROI on the frame
    # while True:
    #     select_roi(frame)
    #     if keyboard.read_key() == "c":
    #         break
    
    for i in range(args.ncrop):
        select_roi(frame)

    # Destroy windows once done
    cv2.destroyAllWindows()

    print(f"Selected ROIs: {len(roi_list)}")
    print(f"ROI Coordinates: {roi_list}")
    print(f"Starting extraction of '{video_name}'")

    try:
        # creating a folder named on the video name
        save_directory = f"{args.out}/{video_name.split('.')[0]}_{str(start_time)}_{str(int(end_time))}"
        if os.path.exists(save_directory):
            shutil.rmtree(save_directory)
        os.makedirs(save_directory)

        os.chdir(save_directory)
        for i in range(len(roi_list)):
            sub_directory = f"crop_{str(i + 1)}"
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)

    # if not created then raise error
    except OSError:
        raise NotADirectoryError("Error: Creating directory")

    while True:
        next_frame = start_time + (current_frame * (1000 / args.fps))
        if next_frame >= end_time:
            break

        # reading from frame
        video.set(cv2.CAP_PROP_POS_MSEC, next_frame)
        frame_exist, frame = video.read()

        if frame_exist:
            crop_index = 1
            # if video is still left continue creating images
            for roi in roi_list:
                save_filename = f"crop_{str(crop_index)}/crop_{str(crop_index)}_{current_frame}_{str(uuid.uuid4())[0:8]}.jpg"
                print(f"Saving cropped frame... {str(current_frame)}")
                cropped_frame = frame[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
                # writing the extracted images
                threading.Thread(target=save_image, args=(save_filename, cropped_frame), daemon=True).start()
                crop_index += 1

            # track how many frames are created
            current_frame += 1
        else:
            break

    with open("coordinates.txt", 'w') as f:
        for line in roi_list:
            f.write(f"{line}\n")
        f.close()
    
    # Release all space
    print(f"Video extraction is finished. Total frames:{current_frame} Total person cropped: {str(len(roi_list))}")
    print(f"Selected ROIs: {len(roi_list)}")
    print(f"ROI Coordinates: {roi_list}")
    print(f"extractted '{video_name}'")
    video.release()