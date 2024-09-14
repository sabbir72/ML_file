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
    # Format time value as hh:mm:ss.milliseconds
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int(microseconds / 1000)  # Convert microseconds to milliseconds

    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:06}"


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


def process_videos_in_directory(video_directory, label, output_base_directory):
    # Iterate over all .mp4 files in the video directory
    for file in os.listdir(video_directory):
        if file.endswith(".mp4"):
            video_path = os.path.join(video_directory, file)
            video_name = os.path.splitext(file)[0]

            # Create unique directories and text files for each video
            video_output_directory = os.path.join(output_base_directory, video_name)
            text_file_path = create_and_save_text_file(video_name, video_output_directory)

            print(f"Processing video: {video_path}")

            # Write frame names to the text file and extract frames
            write_frame_names_to_file(video_path, text_file_path, label, video_output_directory)

    print("All videos processed.")


if __name__ == "__main__":
    # Manually input values
    video_directory = input("Enter the video directory path: ")
    frame_label = input("Enter the label for the frames: ")
    output_base_directory = input("Enter the output base directory path: ")

    # Process videos in the specified directory
    process_videos_in_directory(video_directory, frame_label, output_base_directory)
