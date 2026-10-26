# Copyright (C) 2019 Yukihiko Shinoda
"""Test for media_file."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import TYPE_CHECKING

from parallelmediadownloader.media_file import MediaFile
from parallelmediadownloader.media_file import SaveOrder

if TYPE_CHECKING:
    from pathlib import Path


class TestSaveOrder:
    @staticmethod
    def test(tmp_path: Path) -> None:
        file_name = "20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3"
        save_order = SaveOrder(tmp_path, file_name, datetime(2019, 8, 8, 15, 40, 15, tzinfo=timezone.utc))
        assert save_order.path_file == tmp_path / file_name


class TestMediaFile:
    """Test for MediaFile."""

    @staticmethod
    def test_timestamp(tmp_path: Path, bytes_image_twitter: bytes) -> None:
        """Tests timestamp."""
        file_name = "test.PNG"
        created_date_time = datetime(2019, 8, 8, 2, 28, 15, tzinfo=timezone.utc)
        file_path = tmp_path / file_name
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        MediaFile(bytes_image_twitter, save_order)
        stat = file_path.stat()
        assert stat.st_atime == created_date_time.timestamp()
        assert stat.st_mtime == created_date_time.timestamp()

    @staticmethod
    def test_bytes_remove(tmp_path: Path, bytes_image_twitter: bytes) -> None:
        """Tests bytes and remove()."""
        file_name = "test.PNG"
        created_date_time = datetime(2019, 8, 8, 2, 28, 15, tzinfo=timezone.utc)
        file_path = tmp_path / file_name
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        media_file = MediaFile(bytes_image_twitter, save_order)
        assert file_path.read_bytes() == bytes_image_twitter
        assert media_file.is_filtered is None
        media_file.remove()
        assert not file_path.exists()
