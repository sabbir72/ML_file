import sys
from pathlib import Path

def count_labels(root_path):
    root = Path(f"{root_path}/labels")

    classes = {
        '0': 0,
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0
    }

    categories = {
        '0': 'accessories_handling',
        '1': 'bundling',
        '2': 'machine_setup',
        '3': 'scissoring',
        '4': 'thread_setup',
        '5': 'trimming',
    }

    for file_path in root.glob('*.txt'):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    label = line.strip().split(' ')[0]
                    classes[label] += 1

        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except IOError:
            print(f"An error occurred while reading the file '{file_path}'.")

    start = 0
    print(f"Class index {classes}\n")

    for i, j in classes.items():
        start += j
        print(f'{categories[i]}: {j}')

    print('\nTotal boxes =', start)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_directory>")
    else:
        count_labels(sys.argv[1])