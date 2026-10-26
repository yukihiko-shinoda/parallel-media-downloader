# Copyright (C) 2019 Yukihiko Shinoda
"""Coroutine of downloading media in parallel."""

from __future__ import annotations

import asyncio
from asyncio import Semaphore
from typing import TYPE_CHECKING

import aiohttp

from parallelmediadownloader.media_download_coroutine import MediaDownloadCoroutine
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine

if TYPE_CHECKING:
    from collections.abc import Iterable

    from parallelmediadownloader.media_download_coroutine import DownloadOrder
    from parallelmediadownloader.media_filter import MediaFilter
    from parallelmediadownloader.modeia_download_result import MediaDownloadResult

__all__ = ["ParallelMediaDownloadCoroutine"]


class ParallelMediaDownloadCoroutine:
    """Coroutine of downloading media in parallel."""

    @staticmethod
    async def execute(
        list_download_order: Iterable[DownloadOrder],
        *,
        limit: int = 5,
        media_filter: MediaFilter | None = None,
        allow_http_status: list[int] | None = None,
    ) -> list[MediaDownloadResult]:
        """Download media in parallel."""
        media_download_coroutine = MediaDownloadCoroutine(
            MediaSaveCoroutine(media_filter=media_filter),
            allow_http_status=allow_http_status,
        )
        semaphore = Semaphore(limit)
        async with aiohttp.ClientSession() as client_session:
            tasks = [
                media_download_coroutine.execute(semaphore, client_session, download_order)
                for download_order in list_download_order
            ]
            return await asyncio.gather(*tasks)
