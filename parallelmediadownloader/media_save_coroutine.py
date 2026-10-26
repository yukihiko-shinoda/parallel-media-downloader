# Copyright (C) 2019 Yukihiko Shinoda
"""Coroutine of saving media."""

from __future__ import annotations

from typing import TYPE_CHECKING

from parallelmediadownloader.media_file import MediaFile

if TYPE_CHECKING:
    from parallelmediadownloader.media_file import SaveOrder
    from parallelmediadownloader.media_filter import MediaFilter

__all__ = ["MediaSaveCoroutine"]


class MediaSaveCoroutine:
    """Coroutine of saving media."""

    def __init__(self, *, media_filter: MediaFilter | None = None) -> None:
        self.media_filter = media_filter

    async def execute(self, media: bytes, save_order: SaveOrder) -> MediaFile:
        media_file = MediaFile(media, save_order)
        if self.media_filter is not None and self.media_filter.filter(media_file):
            media_file.remove()
        return media_file
