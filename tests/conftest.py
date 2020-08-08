import pytest
from aioresponses import aioresponses

collect_ignore = ['setup.py']


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mocked:
        yield mocked
