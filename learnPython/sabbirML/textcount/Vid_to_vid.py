import cv2
import os
import argparse
from tqdm import tqdm

def make_video_from_images(image_folder, video_output_path, fps):
    # Get a list of all image files in the directory
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()  # Sort the images to ensure correct sequence

    if not images:
        print("No images found in the specified directory.")
        return

    # Read the first image to get the dimensions
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4 files
    video = cv2.VideoWriter(video_output_path+"output.mp4", fourcc, fps, (width, height))

    for image in tqdm(images, desc="Generating video"):
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    video.release()
    print(f"Video saved as {video_output_path}/output.mp4")

if _name_ == "_main_":
    parser = argparse.ArgumentParser(description="Create a video from images in a directory.")
    parser.add_argument('--src', type=str, help="Path to the folder containing images")
    parser.add_argument('--out', type=str, help="Path to the output video file")
    parser.add_argument('--fps', type=int, default=30, help="Frames per second for the output video (default: 30)")

    args = parser.parse_args()

    make_video_from_images(args.src, args.out, args.fps)