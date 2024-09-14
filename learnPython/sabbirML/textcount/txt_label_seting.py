import os


def update_label_in_range(directory, start_line, end_line, new_label, label_pattern):
    try:
        for file_name in os.listdir(directory):
            if file_name.endswith('.txt'):  # Check for .txt files
                file_path = os.path.join(directory, file_name)
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    if lines:  # Check if the file is not empty
                        print(f"Contents of {file_path} before update:")
                        for line in lines:
                            print(line.strip())  # Print each line of the file

                        for i in range(start_line - 1, end_line):  # Loop through the specified range
                            if i < len(lines):
                                line = lines[i]
                                if label_pattern in line:  # Check if the label pattern is found
                                    # Update the label pattern with the new label value
                                    updated_line = line.replace(label_pattern, f'Label="{new_label}"')
                                    lines[i] = updated_line
                                    print(f"Updated line {i + 1}: {updated_line.strip()}")
                                else:
                                    print(f"Label pattern '{label_pattern}' not found in line {i + 1}")
                        # Write the updated content back to the file
                        with open(file_path, 'w') as file:
                            file.writelines(lines)
                        print(f"\nSuccessfully updated label areas in lines {start_line} to {end_line} in {file_path}")
                    else:
                        print(f"The file '{file_path}' is empty.")
                    return  # Exit function after opening the first .txt file found
        print(f"No .txt files found in the directory '{directory}'.")
    except Exception as e:
        print(f"An error occurred while opening .txt files in the directory '{directory}': {e}")


if __name__ == "__main__":
    # Manually input values
    directory_path = input("Enter the directory path containing the .txt files: ")
    start_line = int(input("Enter the start line number: "))  # Specify the start line (1-based index)
    end_line = int(input("Enter the end line number: "))  # Specify the end line (1-based index, inclusive)
    new_label = input("Enter the new label: ")  # Specify the new label value
    label_pattern = input("Enter the label pattern to search for: ")  # Specify the label pattern

    # Update labels in the specified range
    update_label_in_range(directory_path, start_line, end_line, new_label, label_pattern)
