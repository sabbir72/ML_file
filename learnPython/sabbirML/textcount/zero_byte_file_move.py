import os
import shutil
from pathlib import Path

original_label_path = Path('/home/sabbir/datasets/annotated_data/Associated_Activity_data_update/zip/ZipFile_row/V12_1aug24_asso_work_v12/labels/')
original_image_path = Path('/home/sabbir/datasets/annotated_data/Associated_Activity_data_update/zip/ZipFile_row/V12_1aug24_asso_work_v12/images/')

move_label_path =  Path('/home/sabbir/datasets/annotated_data/Associated_Activity_data_update/zip/ZipFile_row/V12_1aug24_asso_work_v12/zero_label')
move_label_path.mkdir(parents=True, exist_ok=True)

move_image_path =  Path('/home/sabbir/datasets/annotated_data/Associated_Activity_data_update/zip/ZipFile_row/V12_1aug24_asso_work_v12/zero_image')
move_image_path.mkdir(parents=True, exist_ok=True)

for f in original_label_path.iterdir():
    if os.path.getsize(f) == 0:
        txt_file_path = f
        img_file_path = original_image_path/f'{f.stem}.jpg'

        dest_txt_file_path = move_label_path/txt_file_path.name
        dest_img_file_path = move_image_path/img_file_path.name

        shutil.move(txt_file_path, dest_txt_file_path)
        shutil.move(img_file_path, dest_img_file_path)


        # print(txt_file_path)
        # print(dest_txt_file_path)
        # print(img_file_path)
        # print(dest_img_file_path.exists())





        # print(f.name, f.stem, f.suffix)

print("Complete")
