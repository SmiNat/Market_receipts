import os

import pytest

from ..utils import check_if_file_exists, get_list_of_files


def test_get_list_of_files_no_dir():
    dir_path = r"receipts/tests/empty_folder"
    assert os.path.exists(dir_path) is False

    with pytest.raises(FileNotFoundError):
        get_list_of_files(dir_path)


def test_get_list_of_files_empty_dir():
    os.mkdir("receipts/tests/empty_folder")
    dir_path = r"receipts/tests/empty_folder"
    assert os.path.exists(dir_path) is True

    exp_result = []
    assert exp_result.sort() == get_list_of_files(dir_path).sort()
    os.rmdir(dir_path)


def test_get_list_of_files_dir_with_files():
    dir_path = r"receipts/tests/test_data"
    exp_result = [
        "2023-12.csv",
        "invalid_data.csv",
        "2024-04.csv",
    ]
    assert exp_result.sort() == get_list_of_files(dir_path).sort()


def test_check_if_file_exists_with_valid_file(test_file):
    assert check_if_file_exists(test_file) is None


def test_check_if_file_exists_without_a_file():
    file_path = r"receipts/tests/test_data/invalid.csv"

    with pytest.raises(FileNotFoundError) as exc_info:
        check_if_file_exists(file_path)
    assert "File 'receipts/tests/test_data/invalid.csv' was not found" in str(
        exc_info.value
    )
