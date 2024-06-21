import pytest


@pytest.fixture
def test_file():
    return "receipts/tests/test_data/2024-04.csv"


@pytest.fixture
def test_file_invalid():
    return "receipts/tests/test_data/invalid_data.csv"
