import shutil
from pathlib import Path


def remove_files_from_directory(absolute_path_to_directory):
    """
    Remove all files from a directory.

    :param absolute_path_to_directory: the absolute path to the directory to remove
    """
    shutil.rmtree(absolute_path_to_directory)
    Path(absolute_path_to_directory).mkdir(parents=True, exist_ok=True)
