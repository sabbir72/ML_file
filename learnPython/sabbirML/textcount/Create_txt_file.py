import os
import cv2
import random
import string

def create_and_save_text_file(file_name, save_directory):
    # Ensure the directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Define the full path of the text file
    file_path = os.path.join(save_directory, file_name)

    # Create and open the text file for writing
    with open(file_path, 'w') as file:
        print(f"Text file '{file_name}' created in directory '{save_directory}'.")

    return file_path

def generate_random_string(length=8):
    # Generate a random string of specified length containing numbers and lowercase letters
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def format_time(seconds, microseconds):
    # Format time value as hh:mm:ss.microseconds
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if microseconds == 0:
        return f"{hours:02}.{minutes:02}.{seconds:02}.000"
    else:
        return f"{hours:02}.{minutes:02}.{seconds:02}.{str(microseconds)[:3]}"

def write_frame_names_to_file(video_path, text_file_path, label):
    # Extract video name without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Get the frame rate of the video
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    frame_count = 1
    # Write the names of the frame files with labels and time values to the text file
    with open(text_file_path, 'w') as file:
        while True:
            # Read the next frame
            success, frame = video_capture.read()
            if not success:
                break

            # Get the frame position in milliseconds
            time_value_msec = video_capture.get(cv2.CAP_PROP_POS_MSEC)

            # Convert milliseconds to seconds and microseconds
            time_value_sec = time_value_msec / 1000
            microseconds = int((time_value_msec % 1000) * 1000)

            # Calculate the time value for the frame
            time_str = format_time(time_value_sec, microseconds)

            # Generate a unique 8-character string for each frame
            unique_value = generate_random_string()

            # Write the frame name with label, frame number, and time value to the text file
            frame_name = f'{video_name}_{frame_count}_{unique_value}.jpg'
            file.write(f'{frame_name}  Label="{label}"  Time="{time_str}"\n')
            print(f"Added frame name: {frame_name} Label='{label}' Time='{time_str}'")

            # Save the frame as an image file
            cv2.imwrite(os.path.join(save_directory, frame_name), frame)

            frame_count += 1

# Define the file name and save directory for the text file
file_name = 'procrss_scissoring.txt'
save_directory = '/home/sabbir/datasets/home_pc/annotations/cycle_time_demo/label_file/'  # Use single backslash for Windows paths

# Video file path
video_path = '/home/sabbir/datasets/home_pc/annotations/cycle_time_demo/process_01.mp4'  # Replace with the path to your video file

# Manually input label for the frames
frame_label = "get_0"

# Create the text file
file_path = create_and_save_text_file(file_name, save_directory)

# Write the frame names with labels, frame numbers, and time values to the text file and extract frames from the video
write_frame_names_to_file(video_path, file_path, frame_label)

print(f"File path: {file_path}")
