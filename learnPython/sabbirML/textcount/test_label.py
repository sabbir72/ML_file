import os

def update_label_in_range(directory, start_line, end_line, new_label):
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
                        print(f"\nSuccessfully updated label areas in lines {start_line} to {end_line} in {file_path}")
                    else:
                        print(f"The file '{file_path}' is empty.")
                    return  # Exit function after opening the first .txt file found
        print(f"No .txt files found in the directory '{directory}'.")
    except Exception as e:
        print(f"An error occurred while opening .txt files in the directory '{directory}': {e}")

# Example usage
directory_path = '/home/sabbir/datasets/cycle_time/start_cycle/Sleeve_attach/31/output/'

updates = [

    # Add more sets of parameters here
    #
    # {'start_line': 1130, 'end_line': 1147, 'new_label': 'get'},
    # {'start_line': 1171, 'end_line': 1179, 'new_label': 'get'},
    # {'start_line': 1575, 'end_line': 1589, 'new_label': 'get'},
    # # {'start_line': 892, 'end_line': 903, 'new_label': 'get'},
    # # # {'start_line': 2267, 'end_line': 2274, 'new_label': 'get'},
    # # #
    {'start_line': 1590, 'end_line': 1600, 'new_label': 'move'},
    # {'start_line': 1180, 'end_line': 1189, 'new_label': 'move'},
    # {'start_line': 1347, 'end_line': 1384, 'new_label': 'move'},
    # {'start_line': 1385, 'end_line': 1394, 'new_label': 'move'},
    # # #
    # {'start_line': 1216, 'end_line': 1234, 'new_label': 'put'},
    # {'start_line': 1427, 'end_line': 1448, 'new_label': 'put'},
    # #
    {'start_line': 1531, 'end_line': 1542, 'new_label': 'sew'},
    # {'start_line': 1266, 'end_line': 1314, 'new_label': 'sew'},
    # {'start_line': 1449, 'end_line': 1457, 'new_label': 'sew'},
    # {'start_line': 1478, 'end_line': 1509, 'new_label': 'sew'},
    # # #
    {'start_line': 1543, 'end_line': 1574, 'new_label': 'handle'},
    # {'start_line': 1249, 'end_line': 1265, 'new_label': 'handle'},
    # {'start_line': 1315, 'end_line': 1346, 'new_label': 'handle'},
    # {'start_line': 1395, 'end_line': 1426, 'new_label': 'handle'},
    # {'start_line': 1458, 'end_line': 1477, 'new_label': 'handle'},
    #  {'start_line': 1510, 'end_line': 1530, 'new_label': 'handle'},
    # #
    # {'start_line': 1601, 'end_line': 1618, 'new_label': 'dispatch'},
    # {'start_line': 692, 'end_line': 768, 'new_label': 'null'},
]

for update in updates:
    update_label_in_range(directory_path, update['start_line'], update['end_line'], update['new_label'])
