# Copyright (C) 2019 Yukihiko Shinoda
"""Test for media_save_coroutine."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import TYPE_CHECKING

import pytest

from parallelmediadownloader.media_file import SaveOrder
from parallelmediadownloader.media_filter import NotImageFilter
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine

if TYPE_CHECKING:
    from pathlib import Path


class TestMediaSaveCoroutine:
    """Test for MediaSaveCoroutine."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_image(tmp_path: Path, bytes_image_twitter: bytes) -> None:
        """Tests image."""
        file_name = "20190808050245pbs.twimg.com_media_CeBmNUIUUAAZoQ3"
        created_date_time = datetime(2019, 8, 8, 5, 2, 45, tzinfo=timezone.utc)
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        media_file = await MediaSaveCoroutine().execute(bytes_image_twitter, save_order)
        assert media_file.path_file.name == file_name
        assert media_file.path_file.read_bytes() == bytes_image_twitter

    @staticmethod
    @pytest.mark.asyncio
    async def test_filter(tmp_path: Path, bytes_image_twitter: bytes) -> None:
        """Tests filter."""
        file_name = "20190808050245pbs.twimg.com_media_CeBmNUIUUAAZoQ3"
        created_date_time = datetime(2019, 8, 8, 5, 2, 45, tzinfo=timezone.utc)
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        media_file = await MediaSaveCoroutine(media_filter=NotImageFilter()).execute(bytes_image_twitter, save_order)
        assert media_file.path_file.name == file_name
        assert media_file.is_filtered
        assert not media_file.path_file.exists()
