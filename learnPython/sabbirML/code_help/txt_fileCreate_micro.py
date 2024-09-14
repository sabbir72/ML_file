import os
import cv2
import random
import string

def create_and_save_text_file(file_name, save_directory):
    # Ensure the directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Append .txt extension to the file name
    file_name_with_extension = file_name + ".txt"

    # Define the full path of the text file
    file_path = os.path.join(save_directory, file_name_with_extension)

    # Create and open the text file for writing
    with open(file_path, 'w') as file:
        print(f"Text file '{file_name_with_extension}' created in directory '{save_directory}'.")

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
        return f"{hours:02}:{minutes:02}:{seconds:02}.000000"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:02}.{str(microseconds)[:06]}"

# Convert hh:mm:ss to seconds
def time_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}. Expected format is hh:mm:ss")

# Convert seconds to milliseconds
def to_milliseconds(seconds: int) -> int:
    return int(seconds * 1000)

def write_frame_names_to_file(video_path, text_file_path, label, save_directory):
    # Extract video name without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    frame_count = 0
    # Write the names of the frame files with labels and time values to the text file
    with open(text_file_path, 'w') as file:
        while True:
            # Read the next frame
            success, frame = video_capture.read()
            if not success:
                break

            # Convert milliseconds to seconds and microseconds
            time_value_msec = video_capture.get(cv2.CAP_PROP_POS_MSEC)
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

    print(f"Video '{video_name}' processed. Total frames: {frame_count}")

def process_videos_in_directory(video_directory, file_name, label, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Create the text file
    text_file_path = create_and_save_text_file(file_name, output_directory)

    # Iterate over all .mp4 files in the video directory
    for file in os.listdir(video_directory):
        if file.endswith(".mp4"):
            video_path = os.path.join(video_directory, file)
            print(f"Processing video: {video_path}")

            # Write frame names to the text file and extract frames
            write_frame_names_to_file(video_path, text_file_path, label, output_directory)

    print(f"All videos processed. File path: {text_file_path}")

if __name__ == "__main__":
    # Manually input values
    video_directory = input("Enter the video directory path: ")
    file_name = input("Enter the text file name: ")
    frame_label = input("Enter the label for the frames: ")
    output_directory = input("Enter the output directory path: ")

    # Process videos in the specified directory
    process_videos_in_directory(video_directory, file_name, frame_label, output_directory)
