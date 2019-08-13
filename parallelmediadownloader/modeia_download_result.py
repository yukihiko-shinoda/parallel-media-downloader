from dataclasses import dataclass

from parallelmediadownloader.media_file import MediaFile


@dataclass
class MediaDownloadResult:
    url: str
    status: int
    media_file: MediaFile
