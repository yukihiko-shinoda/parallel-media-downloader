# Copyright (C) 2019 Yukihiko Shinoda
"""Aggregation of media download result."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parallelmediadownloader.media_file import MediaFile

__all__ = ["MediaDownloadResult"]


@dataclass
class MediaDownloadResult:
    url: str
    status: int
    media_file: MediaFile | None
