from datetime import datetime

import pytest
from parallelmediadownloader.media_file import SaveOrder
from parallelmediadownloader.media_filter import NotImageFilter
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine
from tests.testlibraries.instance_resource import InstanceResource


class TestMediaSaveCoroutine:
    @staticmethod
    @pytest.mark.asyncio
    async def test_image(tmp_path):
        file_name = '20190808050245pbs.twimg.com_media_CeBmNUIUUAAZoQ3'
        created_date_time = datetime(2019, 8, 8, 5, 2, 45)
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        media_file = await MediaSaveCoroutine().execute(
            InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes(), save_order
        )
        assert media_file.path_file.name == file_name
        assert media_file.path_file.read_bytes() == InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes()

    @staticmethod
    @pytest.mark.asyncio
    async def test_filter(tmp_path):
        file_name = '20190808050245pbs.twimg.com_media_CeBmNUIUUAAZoQ3'
        created_date_time = datetime(2019, 8, 8, 5, 2, 45)
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        media_file = await MediaSaveCoroutine(media_filter=NotImageFilter()).execute(
            InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes(), save_order
        )
        assert media_file.path_file.name == file_name
        assert media_file.is_filtered
        assert not media_file.path_file.exists()
