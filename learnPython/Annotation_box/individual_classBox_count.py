from pathlib import Path


root = Path('/home/sabbir/datasets/annotated_data/Associate/without_obyte_file/22Apr24_ass_work_v0/labels')
d = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
for file_path in root.glob('*.txt'):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                s = line.strip().split(' ')[0]
                d[s] += 1
                if s == '1':
                    print(file_path)

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except IOError:
        print(f"An error occurred while reading the file '{file_path}'.")

start =0
print(d)
for i,j in d.items():
    start += j
    print(f'category {i} found {d[i]}')

print('total box = ', start)

#print(d.keys(), d.values(),d.items())

