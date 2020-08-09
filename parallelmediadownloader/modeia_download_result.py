"""Aggregation of media download result."""
from dataclasses import dataclass
from typing import Optional

from parallelmediadownloader.media_file import MediaFile


@dataclass
class MediaDownloadResult:
    url: str
    status: int
    media_file: Optional[MediaFile]
