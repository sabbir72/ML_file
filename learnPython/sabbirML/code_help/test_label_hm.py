import os
def update_labels_in_ranges(directory, ranges, new_label):
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

                        for start_line, end_line in ranges:
                            for i in range(start_line - 1, end_line):  # Loop through the specified range
                                if i < len(lines):
                                    line = lines[i]
                                    # Find the label pattern
                                    label_pattern = 'class'  # Pre label add
                                    if label_pattern in line:  # Check if the label pattern is found
                                        # Update the label pattern with the new label value
                                        updated_line = line.replace(label_pattern, f'{new_label}')
                                        lines[i] = updated_line
                                        print(f"Updated line {i + 1}: {updated_line.strip()}")
                                    else:
                                        print(f"Label pattern not found in line {i + 1}")
                        # Write the updated content back to the file
                        with open(file_path, 'w') as file:
                            file.writelines(lines)
                        print(f"\nSuccessfully updated label areas in {file_path}")
                    else:
                        print(f"The file '{file_path}' is empty.")
                    return  # Exit function after opening the first .txt file found
        print(f"No .txt files found in the directory '{directory}'.")
    except Exception as e:
        print(f"An error occurred while opening .txt files in the directory '{directory}': {e}")
# Example usage
directory_path = '/home/sabbir/datasets/cycle_time/20fps/Bottom_rib_attach/225/'
ranges = [
    (576,594),
    (1055,1083),
    #
    # (882,913),
    # (992,1054),
    # #
    # (612,630),
    # (647,719),
    # (740,881),
    # (914,991),
    # (1539,1581),

]
# new_label = 'get'
# new_label = 'handle'
# new_label = 'put'
# new_label = 'sew'
new_label = 'dispatch'
# new_label = 'TP_dispatch'
# new_label = 'null'
# new_label = 'class'
# new_label = 'trim'


update_labels_in_ranges(directory_path, ranges, new_label)
