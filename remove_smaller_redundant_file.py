"""
When Shotwell encounters files with the same name and same EXIF date time, it renames file name as _1.
There is no guarantee which one (with or without _1) is larger.
This program deletes the smaller one.
Log file is generated under the same directory as the Python file.
"""

import glob
import logging
import os
import re

logging.basicConfig(filename='remove_smaller_redundant_file.log', encoding='utf-8', level=logging.INFO)

logging.info(f"==================One Run=====================")

# See https://docs.python.org/3/library/glob.html for format.
to_be_processed_folder = "/home/ye/test/**/*_1.*"


def process_folder(folder_path_pattern):
    deleted_file_count = 0
    no_match_count = 0
    with_1_file_deletion_count = 0
    without_1_file_deletion_count = 0

    for file in glob.iglob(folder_path_pattern, recursive=True):
        # Result IMG_20170813_180001_1.jpg
        source_file_name = os.path.basename(file)
        # Result IMG_20170813_180001.jpg
        file_name_without_1 = re.sub("_1\.", ".", source_file_name)

        current_directory_name = os.path.dirname(file)
        file_name_without_1_path_file_name = os.path.join(current_directory_name, file_name_without_1)
        is_file_name_without_1_file_existing = os.path.isfile(file_name_without_1_path_file_name)

        if is_file_name_without_1_file_existing:
            source_file_size = os.path.getsize(file)
            file_name_without_1_file_size = os.path.getsize(file_name_without_1_path_file_name)
            if source_file_size > file_name_without_1_file_size:
                os.remove(file_name_without_1_path_file_name)
                without_1_file_deletion_count += 1
                logging.info(f"Deleted {file_name_without_1_path_file_name}, size {file_name_without_1_file_size}; "
                             f"Kept {source_file_size} size {file}")
            else:
                os.remove(file)
                with_1_file_deletion_count += 1
                logging.info(f"Deleted {file}, size {source_file_size}; "
                             f"Kept {file_name_without_1_file_size} size, {file_name_without_1_path_file_name}")

            deleted_file_count += 1
        else:
            no_match_count += 1

    logging.info(f"{no_match_count} _1 files has no matching file")
    logging.info(f"Total deleted file count {deleted_file_count}")
    logging.info(f"Deleted *_1 count: {with_1_file_deletion_count}")
    logging.info(f"Deleted without 1 count: {without_1_file_deletion_count}")


if __name__ == '__main__':
    process_folder(to_be_processed_folder)
    print("Done!")
