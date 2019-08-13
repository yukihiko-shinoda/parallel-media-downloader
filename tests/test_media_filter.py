from datetime import datetime

import pytest

from parallelmediadownloader.media_file import SaveOrder, MediaFile
from parallelmediadownloader.media_filter import NotImageFilter, MediaFilter
from tests.testlibraries.instance_resource import InstanceResource


class TestMediaFilter:
    @staticmethod
    def test(tmp_path):
        save_order = SaveOrder(tmp_path, 'test.PNG', datetime(2019, 8, 8, 2, 28, 15))
        media_file = MediaFile(InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes(), save_order)
        assert not NotImageFilter().filter(media_file)
        assert not media_file.is_filtered

    @staticmethod
    def test_is_micro_image_not_image_file(tmp_path):
        save_order = SaveOrder(tmp_path, 'test.mp4', datetime(2019, 8, 8, 2, 28, 15))
        media_file = MediaFile(InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes(), save_order)
        assert NotImageFilter().filter(media_file)
        assert media_file.is_filtered

    @staticmethod
    def test_not_implemented_error(tmp_path):
        class ErrorFilter(MediaFilter):
            def _filter(self, media_file: MediaFile):
                super()._filter(media_file)
                assert False
        save_order = SaveOrder(tmp_path, 'test.PNG', datetime(2019, 8, 8, 2, 28, 15))
        with pytest.raises(NotImplementedError):
            ErrorFilter().filter(MediaFile(InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes(), save_order))
