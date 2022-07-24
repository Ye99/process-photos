import glob


def process_file(file_name):
    print(file_name)


# Folder to be processed. See https://docs.python.org/3/library/glob.html for format.
folder_path = "/home/ye/Pictures/2018/2018_09_08/*"


def process_folder(folder_path_pattern):
    total_file = 0

    for file in glob.iglob(folder_path_pattern, recursive=False):
        total_file += 1
        process_file(file)

    print(f"Total file {total_file}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process_folder(folder_path)
