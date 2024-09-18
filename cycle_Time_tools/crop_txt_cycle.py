
import os
import cv2
import random
import string


def create_and_save_text_file(file_name, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    file_name_with_extension = file_name + ".txt"
    file_path = os.path.join(save_directory, file_name_with_extension)
    with open(file_path, 'w') as file:
        print(f"Text file '{file_name_with_extension}' created in directory '{save_directory}'.")
    return file_path


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def format_time(seconds, microseconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int(microseconds / 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:06}"


def select_rois(frame, num_rois, video_name):
    rois = []
    for i in range(num_rois):
        cv2.namedWindow(video_name, cv2.WINDOW_NORMAL)
        height, width = frame.shape[:2]
        # cv2.resizeWindow("Select ROI", width, height)
        # cv2.imshow("Select ROI", frame)

        roi = cv2.selectROI(video_name, frame, fromCenter=False, showCrosshair=True)
        if roi == (0, 0, 0, 0):
            break

        # Draw ROI in blue
        x, y, w, h = roi
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.imshow("Select ROI", frame)
        cv2.waitKey(1)

        # Finalize ROI by drawing in green
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.imshow("Select ROI", frame)
        cv2.waitKey(1)

        rois.append(roi)

    cv2.destroyWindow(video_name)
    return rois


def write_frame_names_to_files(video_path, base_text_file_path, label, save_directory, target_fps, num_crops):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_capture = cv2.VideoCapture(video_path)
    original_fps = video_capture.get(cv2.CAP_PROP_FPS)

    frame_count = 0
    frame_interval = int(original_fps / target_fps)  # Calculate interval to sample target FPS
    frame_counter = 0

    success, frame = video_capture.read()
    if not success:
        print("Error: Unable to read the first frame.")
        return

    rois = select_rois(frame, num_crops, video_name)
    if not rois:
        print("No ROIs selected. Exiting.")
        return

    text_files = []
    roi_directories = []

    for i in range(len(rois)):
        roi_dir = os.path.join(save_directory, f'person_{i + 1}')
        if not os.path.exists(roi_dir):
            os.makedirs(roi_dir)
        roi_directories.append(roi_dir)
        text_file_path = os.path.join(roi_dir, f'{video_name}_person_{i + 1}.txt')
        text_files.append(text_file_path)
        # create_and_save_text_file(f'{video_name}_per{i + 1}', roi_dir)

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        if frame_counter % frame_interval == 0:
            time_value_msec = video_capture.get(cv2.CAP_PROP_POS_MSEC)
            time_value_sec = time_value_msec / 1000
            microseconds = int((time_value_msec % 1000) * 1000)
            time_str = format_time(time_value_sec, microseconds)

            for i, (x, y, w, h) in enumerate(rois):
                unique_value = generate_random_string()
                cropped_frame = frame[y:y + h, x:x + w]

                # _roi{i + 1}  future need use
                frame_name = f'{video_name}_{frame_count}_{unique_value}.jpg'
                file_path = text_files[i]
                with open(file_path, 'a') as roi_file:
                    roi_file.write(f'{frame_name}  {label}  {time_str} \n') 
                    print(f"Added frame name: {frame_name} Label={label} Time={time_str} ")
                cv2.imwrite(os.path.join(roi_directories[i], frame_name), cropped_frame)

            frame_count += 1

        frame_counter += 1

    print(f"Video '{video_name}' processed. Total frames: {frame_count}")


def process_videos_in_directory(video_directory, label, output_base_directory, fps, num_crops):
    for file in os.listdir(video_directory):
        if file.endswith(".mp4"):
            video_path = os.path.join(video_directory, file)
            video_name = os.path.splitext(file)[0]
            video_output_directory = os.path.join(output_base_directory, video_name)

            print(f"Processing video: {video_path}")
            write_frame_names_to_files(video_path, video_output_directory, label, video_output_directory, fps,
                                       num_crops)

    print("All videos processed.")


if __name__ == "__main__":
    video_directory = input("Enter the video directory path: ")
    frame_label = input("Enter frames default label Name : ")
    output_base_directory = input("Enter the output directory path: ")
    fps = float(input("Enter the target (FPS) : "))
    num_crops = int(input("Enter the number of crops: "))

    process_videos_in_directory(video_directory, frame_label, output_base_directory, fps, num_crops)


