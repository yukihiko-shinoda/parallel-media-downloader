# Copyright (C) 2019 Yukihiko Shinoda
"""API of parallel media downloading."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from parallelmediadownloader.parallel_media_download_coroutine import ParallelMediaDownloadCoroutine

if TYPE_CHECKING:
    from collections.abc import Iterable

    from parallelmediadownloader.media_download_coroutine import DownloadOrder
    from parallelmediadownloader.media_filter import MediaFilter
    from parallelmediadownloader.modeia_download_result import MediaDownloadResult

__all__ = ["ParallelMediaDownloader"]


class ParallelMediaDownloader:
    """API of parallel media downloading."""

    @staticmethod
    def execute(
        list_download_order: Iterable[DownloadOrder],
        *,
        limit: int = 5,
        media_filter: MediaFilter | None = None,
        # Reason: To be this method as non async. pylint: disable=duplicate-code
        allow_http_status: list[int] | None = None,
    ) -> list[MediaDownloadResult]:
        """Execute parallel media downloading."""
        return asyncio.run(
            ParallelMediaDownloadCoroutine.execute(
                list_download_order,
                limit=limit,
                media_filter=media_filter,
                allow_http_status=allow_http_status,
            ),
        )
