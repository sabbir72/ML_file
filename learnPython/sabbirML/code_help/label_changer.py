import os

files = []

# Add the path of txt folder

# file path here input
path = "/home/sabbir/datasets/annotated_data/Associated_Activity_data_update/V10.4_27june24_asso_work_v10.4/labels/train/"
for i in os.listdir(path):
    if i.endswith('.txt'):
        files.append(i)

for item in files:
    # define an empty list
    file_data = []

    with open(os.path.join(path, item), 'r') as myfile:
        print(myfile)
        for line in myfile:
            # remove linebreak which is the last character of the string
            currentLine = line.strip()
            data = currentLine.split(" ")
            # add item to the list
            file_data.append(data)
    
    # Decrease the first number in any line by one
    for i in file_data:
        if i[0] == '4':    ## previous label
            i[0] = '5'     ## updated label
        elif i[0] == '5':
            i[0] = '4'

    # Write back to the same file
    with open(os.path.join(path, item), 'w') as f:
        for i in file_data:
            res = " ".join(i)
            f.write(res + "\n")
