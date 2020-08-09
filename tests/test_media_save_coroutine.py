"""Test for media_save_coroutine."""
from datetime import datetime

import pytest

from parallelmediadownloader.media_file import SaveOrder
from parallelmediadownloader.media_filter import NotImageFilter
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine


class TestMediaSaveCoroutine:
    """Test for MediaSaveCoroutine."""

    @staticmethod
    @pytest.mark.asyncio
    async def test_image(tmp_path, bytes_image_twitter):
        """Tests image."""
        file_name = "20190808050245pbs.twimg.com_media_CeBmNUIUUAAZoQ3"
        created_date_time = datetime(2019, 8, 8, 5, 2, 45)
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        media_file = await MediaSaveCoroutine().execute(bytes_image_twitter, save_order)
        assert media_file.path_file.name == file_name
        assert media_file.path_file.read_bytes() == bytes_image_twitter

    @staticmethod
    @pytest.mark.asyncio
    async def test_filter(tmp_path, bytes_image_twitter):
        """Tests filter."""
        file_name = "20190808050245pbs.twimg.com_media_CeBmNUIUUAAZoQ3"
        created_date_time = datetime(2019, 8, 8, 5, 2, 45)
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        media_file = await MediaSaveCoroutine(media_filter=NotImageFilter()).execute(bytes_image_twitter, save_order)
        assert media_file.path_file.name == file_name
        assert media_file.is_filtered
        assert not media_file.path_file.exists()
