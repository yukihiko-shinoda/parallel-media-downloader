# Copyright (C) 2019 Yukihiko Shinoda
"""Media filters."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parallelmediadownloader.media_file import MediaFile

__all__ = ["MediaFilter", "NotImageFilter"]


class MediaFilter(ABC):
    """Base class of media filter."""

    def filter(self, media_file: MediaFile) -> bool:
        is_filtered = self._filter(media_file)
        media_file.is_filtered = is_filtered
        return is_filtered

    @abstractmethod
    def _filter(self, media_file: MediaFile) -> bool:
        raise NotImplementedError


class NotImageFilter(MediaFilter):
    def _filter(self, media_file: MediaFile) -> bool:
        return not str(media_file.path_file).lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
