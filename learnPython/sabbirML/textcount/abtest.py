import cv2
import os


# Function to create directories if they don't exist
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


# Path to the trainlist file
trainlist_path = '/home/sabbir/datasets/home_pc/z_test/crop_1/a_path/'

# Base output directory for frames
output_dir = '/home/sabbir/datasets/home_pc/z_test/crop_1/b_output/'

# Read the trainlist file
with open(trainlist_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        category_path = parts[0]
        label = int(parts[1])

        # Extract category and video file path
        category, video_filename = category_path.split('/')
        video_path = os.path.join('/home/sabbir/datasets/home_pc/z_test/crop_1/', category_path)  # Adjust base path as needed

        # Create directory for output frames if not exists
        output_category_dir = os.path.join(output_dir, category)
        ensure_dir(output_category_dir)

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_filename = f"{video_filename}_frame_{frame_count:05d}.jpg"
            frame_path = os.path.join(output_category_dir, frame_filename)

            # Save the frame as an image file
            cv2.imwrite(frame_path, frame)

            # Create the corresponding text file with label
            txt_filename = f"{video_filename}_frame_{frame_count:05d}.txt"
            txt_path = os.path.join(output_category_dir, txt_filename)

            with open(txt_path, 'w') as txt_file:
                txt_file.write(f"{category}/{frame_filename} {label}\n")

            frame_count += 1

        cap.release()

print("Frame extraction and text file creation complete.")
