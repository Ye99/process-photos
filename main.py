import glob
import os
from dateutil import parser
import shutil

# Points to parent folder of the to be created 2016, 2017 etc folders.
output_folder = "/home/ye/2017_2018_Master/"


def extract_date(file_name):
    try:
        # https://dateutil.readthedocs.io/en/stable/parser.html
        return parser.parse(file_name, fuzzy=True)
    except:
        print(f"Pass error {file_name}")


def process_file(source_path_file_name):
    source_file_name = os.path.basename(source_path_file_name)

    date = extract_date(source_file_name)

    if date:
        target_year_folder = os.path.join(output_folder, str(date.year))
        is_target_year_folder_existing = os.path.isdir(target_year_folder)

        if not is_target_year_folder_existing:
            os.mkdir(target_year_folder)

        # Build yyyy_mm_dd folder string
        month = date.strftime("%m")
        day = date.strftime("%d")
        yyyy_mm_dd = f"{date.year}_{month}_{day}"
        target_year_date_folder = os.path.join(output_folder, str(date.year), yyyy_mm_dd)
        is_target_year_date_folder_existing = os.path.isdir(target_year_date_folder)

        if not is_target_year_date_folder_existing:
            os.mkdir(target_year_date_folder)

        target_path_file_name = os.path.join(target_year_date_folder, source_file_name)
        is_file_exist_at_target_folder = os.path.isfile(target_path_file_name)

        if is_file_exist_at_target_folder:
            source_file_size = os.path.getsize(source_path_file_name)
            targe_file_size = os.path.getsize(target_path_file_name)
            if source_file_size > targe_file_size:
                shutil.move(source_path_file_name, target_path_file_name)
                print(f"overwrite target file {target_path_file_name} with larger source file {source_path_file_name}")
            else:
                print(f"skip and remove source file {source_path_file_name} because existing target file is larger")
                os.remove(source_path_file_name)
        else:
            shutil.move(source_path_file_name, target_path_file_name)
            print(f"moved source file {source_path_file_name} to {target_path_file_name}")


# Folder to be processed. See https://docs.python.org/3/library/glob.html for format.
folder_path = "/home/ye/2017_2018_Master/2016/2016 2月至7月 时丽君拍的/*"


def process_folder(folder_path_pattern):
    total_file = 0

    for file in glob.iglob(folder_path_pattern, recursive=False):
        total_file += 1
        process_file(file)

    print(f"Total file {total_file}")


if __name__ == '__main__':
    process_folder(folder_path)
