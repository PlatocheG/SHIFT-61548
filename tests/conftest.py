import pytest

from config import TEST_API_URL

API_URL = TEST_API_URL

def pytest_addoption(parser):
    parser.addoption(
        "--test",
        default = "fast",
        choices = ("fast", "all")
    )
