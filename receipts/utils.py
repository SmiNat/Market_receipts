import os


def check_if_file_exists(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundError("File '%s' was not found." % file_path)


def get_list_of_files(dir_path: str) -> list[str]:
    files = os.listdir(dir_path)
    return files
