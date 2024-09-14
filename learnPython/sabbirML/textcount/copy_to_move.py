import os
import shutil


def copy_top_10_images(source_folder, destination_folder):
    # Ensure destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate over each folder in the source directory
    for root, dirs, files in os.walk(source_folder):
        # Get the name of the current folder
        folder_name = os.path.basename(root)

        # Filter out only image files (assuming images have extensions like .jpg, .png, etc.)
        image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

        # Sort image files based on modification time (you can change this to any sorting criteria you prefer)
        image_files.sort(key=lambda x: os.path.getmtime(os.path.join(root, x)))

        # Copy the top ten image files from the current folder to the destination folder
        for i, file in enumerate(image_files[:10]):
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_folder, folder_name + "_" + file)
            shutil.copyfile(source_file, destination_file)
            print(f"Copied: {source_file} to {destination_file}")


if __name__ == "__main__":
    source_folder = input("Enter the path of the source folder: ")
    destination_folder = input("Enter the path of the destination folder: ")

    copy_top_10_images(source_folder, destination_folder)
