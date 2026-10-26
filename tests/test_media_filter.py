# Copyright (C) 2019 Yukihiko Shinoda
"""Test for media_filter."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import TYPE_CHECKING

from parallelmediadownloader.media_file import MediaFile
from parallelmediadownloader.media_file import SaveOrder
from parallelmediadownloader.media_filter import NotImageFilter

if TYPE_CHECKING:
    from pathlib import Path


class TestMediaFilter:
    """Test for MediaFilter."""

    @staticmethod
    def test(tmp_path: Path, bytes_image_twitter: bytes) -> None:
        save_order = SaveOrder(tmp_path, "test.PNG", datetime(2019, 8, 8, 2, 28, 15, tzinfo=timezone.utc))
        media_file = MediaFile(bytes_image_twitter, save_order)
        assert not NotImageFilter().filter(media_file)
        assert not media_file.is_filtered

    @staticmethod
    def test_is_micro_image_not_image_file(tmp_path: Path, bytes_image_twitter: bytes) -> None:
        save_order = SaveOrder(tmp_path, "test.mp4", datetime(2019, 8, 8, 2, 28, 15, tzinfo=timezone.utc))
        media_file = MediaFile(bytes_image_twitter, save_order)
        assert NotImageFilter().filter(media_file)
        assert media_file.is_filtered
