"""Media filters."""
from abc import ABC, abstractmethod

from parallelmediadownloader.media_file import MediaFile

__all__ = ["MediaFilter", "NotImageFilter"]


class MediaFilter(ABC):
    """Base class of media filter."""

    def filter(self, media_file: MediaFile) -> bool:
        media_file.is_filtered = self._filter(media_file)
        return media_file.is_filtered

    @abstractmethod
    def _filter(self, media_file: MediaFile) -> bool:
        raise NotImplementedError()


class NotImageFilter(MediaFilter):
    def _filter(self, media_file: MediaFile) -> bool:
        return not str(media_file.path_file).lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
