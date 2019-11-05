#!/usr/bin/env python
import asyncio
from typing import List, Iterable, Optional

from parallelmediadownloader.media_download_coroutine import DownloadOrder
from parallelmediadownloader.media_filter import MediaFilter
from parallelmediadownloader.parallel_media_download_coroutine import ParallelMediaDownloadCoroutine
from parallelmediadownloader.modeia_download_result import MediaDownloadResult


class ParallelMediaDownloader:
    @staticmethod
    def execute(list_download_order: Iterable[DownloadOrder], *,
                limit: int = 5, media_filter: Optional[MediaFilter] = None, allow_http_status: List[int] = None
                ) -> List[MediaDownloadResult]:
        return asyncio.get_event_loop().run_until_complete(
            ParallelMediaDownloadCoroutine.execute(
                list_download_order, limit=limit, media_filter=media_filter, allow_http_status=allow_http_status
            )
        )
