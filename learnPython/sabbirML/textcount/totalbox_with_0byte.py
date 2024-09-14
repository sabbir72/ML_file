import os

def count_lines_in_folder(folder_path):
    """Count the number of lines in each text file inside a folder."""
    line_count = 0
    zero_byte_files = 0  # Counter for 0-byte size files
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    zero_byte_files += 1
                else:
                    with open(file_path, 'r') as file:
                        line_count += sum(1 for line in file)
    return line_count, zero_byte_files

def main():
    folder_path = r'/home/sabbir/datasets/annotated_data/Associate/22Apr24_ass_work_v2/labels'  # Change this to the desired folder path
    total_lines, zero_byte_files = count_lines_in_folder(folder_path)
    print(f"Total number of lines in all .txt files: {total_lines}")
    print(f"Number of 0-byte size .txt files: {zero_byte_files}")

if __name__ == "__main__":
    main()
