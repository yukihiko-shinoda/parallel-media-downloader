"""Model for media file."""
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

__all__ = ["SaveOrder", "MediaFile"]


@dataclass
class SaveOrder:
    """Aggregation of save order."""

    path_directory_download: Path
    file_name: str
    created_date_time: datetime

    @property
    def path_file(self) -> Path:
        return self.path_directory_download / self.file_name


class MediaFile:
    """Model for media file."""

    def __init__(self, media: bytes, save_order: SaveOrder):
        self.path_file = save_order.path_file
        self.is_filtered: Optional[bool] = None
        with self.path_file.open("wb") as file:
            file.write(media)
        seconds = save_order.created_date_time.timestamp()
        os.utime(str(self.path_file), (seconds, seconds))

    def remove(self) -> None:
        os.remove(str(self.path_file))
