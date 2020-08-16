"""Coroutine of downloading media in parallel."""
import asyncio
from asyncio import Semaphore
from typing import Iterable, List, Optional

import aiohttp

from parallelmediadownloader.media_download_coroutine import DownloadOrder, MediaDownloadCoroutine
from parallelmediadownloader.media_filter import MediaFilter
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine
from parallelmediadownloader.modeia_download_result import MediaDownloadResult

__all__ = ["ParallelMediaDownloadCoroutine"]


class ParallelMediaDownloadCoroutine:
    """Coroutine of downloading media in parallel."""

    @staticmethod
    async def execute(
        list_download_order: Iterable[DownloadOrder],
        *,
        limit: int = 5,
        media_filter: Optional[MediaFilter] = None,
        allow_http_status: List[int] = None
    ) -> List[MediaDownloadResult]:
        """Downloads media in parallel."""
        media_download_coroutine = MediaDownloadCoroutine(
            MediaSaveCoroutine(media_filter=media_filter), allow_http_status=allow_http_status
        )
        semaphore = Semaphore(limit)
        async with aiohttp.ClientSession() as client_session:
            tasks = [
                media_download_coroutine.execute(semaphore, client_session, download_order)
                for download_order in list_download_order
            ]
            return await asyncio.gather(*tasks)  # type: ignore
