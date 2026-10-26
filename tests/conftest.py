# Copyright (C) 2019 Yukihiko Shinoda
"""Configuration for pytest."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import TYPE_CHECKING

import pytest
from aioresponses import aioresponses

from parallelmediadownloader.media_download_coroutine import DownloadOrder
from parallelmediadownloader.media_file import SaveOrder
from tests.testlibraries.instance_resource import InstanceResource

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path


@pytest.fixture
def mock_aioresponse() -> Generator[aioresponses, None, None]:
    with aioresponses() as mocked:
        yield mocked


@pytest.fixture
def bytes_image_twitter(resource_path_root: Path) -> bytes:
    return (resource_path_root / "image_twitter.jpg").read_bytes()


@pytest.fixture
def download_order(tmp_path: Path) -> DownloadOrder:
    return DownloadOrder(
        InstanceResource.URL_TWITTER_IMAGE,
        SaveOrder(
            tmp_path,
            "20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3",
            datetime(2019, 8, 8, 15, 40, 15, tzinfo=timezone.utc),
        ),
    )
