"""Configuration for pytest."""
import pytest
from aioresponses import aioresponses  # type: ignore

collect_ignore = ["setup.py"]


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mocked:
        yield mocked


@pytest.fixture
def bytes_image_twitter(resource_path_root):
    yield (resource_path_root / "image_twitter.jpg").read_bytes()
