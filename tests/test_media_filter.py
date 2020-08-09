"""Test for media_filter."""
from datetime import datetime

import pytest

from parallelmediadownloader.media_file import MediaFile, SaveOrder
from parallelmediadownloader.media_filter import MediaFilter, NotImageFilter


class TestMediaFilter:
    """Test for MediaFilter."""

    @staticmethod
    def test(tmp_path, bytes_image_twitter):
        save_order = SaveOrder(tmp_path, "test.PNG", datetime(2019, 8, 8, 2, 28, 15))
        media_file = MediaFile(bytes_image_twitter, save_order)
        assert not NotImageFilter().filter(media_file)
        assert not media_file.is_filtered

    @staticmethod
    def test_is_micro_image_not_image_file(tmp_path, bytes_image_twitter):
        save_order = SaveOrder(tmp_path, "test.mp4", datetime(2019, 8, 8, 2, 28, 15))
        media_file = MediaFile(bytes_image_twitter, save_order)
        assert NotImageFilter().filter(media_file)
        assert media_file.is_filtered

    @staticmethod
    def test_not_implemented_error(tmp_path, bytes_image_twitter):
        """Test NotImplementedError."""

        class ErrorFilter(MediaFilter):
            def _filter(self, media_file: MediaFile):
                super()._filter(media_file)
                assert False

        save_order = SaveOrder(tmp_path, "test.PNG", datetime(2019, 8, 8, 2, 28, 15))
        with pytest.raises(NotImplementedError):
            ErrorFilter().filter(MediaFile(bytes_image_twitter, save_order))
