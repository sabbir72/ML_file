'''
import os

def count_lines_in_file(file_path):
    """Count the number of lines in a file."""
    with open(file_path, 'r') as file:
        return sum(1 for line in file)

def find_files_with_multiple_lines(folder_path):
    """Find text files with two or more lines."""
    multiline_files = []

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                line_count = count_lines_in_file(file_path)
                if line_count >= 2:
                    multiline_files.append(file_name)

    return multiline_files

def main():
    folder_path = r'/home/sabbir/Downloads/pro/labels'  # Change this to the desired folder path
    multiline_files = find_files_with_multiple_lines(folder_path)
    if multiline_files:
        print("Text files with two or more lines:")
        for file_name in multiline_files:
            print(file_name)
        print("Total count:", len(multiline_files))
    else:
        print("No text files with two or more lines found.")

if __name__ == "__main__":
    main()
'''

import os
import shutil
from pathlib import Path

def count_lines_in_file(file_path):
    """Count the number of lines in a file."""
    with open(file_path, 'r') as file:
        return sum(1 for line in file)

original_label_path = Path('/home/sabbir/datasets/299132_file_name_check_demo-20240514T053701Z-001/299132_file_name_check_demo/labels/')
original_image_path = Path('/home/sabbir/datasets/299132_file_name_check_demo-20240514T053701Z-001/299132_file_name_check_demo/images/')

move_label_path = Path('/home/sabbir/datasets/299132_file_name_check_demo-20240514T053701Z-001/299132_file_name_check_demo/twoline_label')
move_label_path.mkdir(parents=True, exist_ok=True)

move_image_path = Path('/home/sabbir/datasets/299132_file_name_check_demo-20240514T053701Z-001/299132_file_name_check_demo/twoline_image')
move_image_path.mkdir(parents=True, exist_ok=True)

for label_file in original_label_path.iterdir():
    if label_file.is_file():
        # Check if the text file has two or more lines
        if count_lines_in_file(label_file) >= 2:
            # Construct corresponding image file path
            image_file_path = original_image_path / (label_file.stem + '.jpg')

            # Check if the corresponding image file exists
            if image_file_path.exists():
                # Move both text and image files to the destination folders
                shutil.move(label_file, move_label_path / label_file.name)
                shutil.move(image_file_path, move_image_path / image_file_path.name)

print("Complete")
