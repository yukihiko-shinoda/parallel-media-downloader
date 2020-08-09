"""Coroutine of downloading media."""
import asyncio
from asyncio import Semaphore
from dataclasses import dataclass
from logging import getLogger
from typing import List

from aiohttp import ClientConnectorError, ClientResponseError, ClientSession

from parallelmediadownloader.exceptions import HttpTimeoutError
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine, SaveOrder
from parallelmediadownloader.modeia_download_result import MediaDownloadResult

logger = getLogger(__name__)


@dataclass
class DownloadOrder:
    url: str
    save_order: SaveOrder


class MediaDownloadCoroutine:
    """Coroutine of downloading media."""

    def __init__(self, media_save_coroutine: MediaSaveCoroutine, *, allow_http_status: List[int] = None):
        self.media_save_coroutine = media_save_coroutine
        self.allow_http_status = [] if allow_http_status is None else allow_http_status

    async def execute(
        self, semaphore: Semaphore, client_session: ClientSession, download_order: DownloadOrder
    ) -> MediaDownloadResult:
        """function want to limit the number of parallel"""
        url = download_order.url
        async with semaphore:
            try:
                response = await client_session.get(url, timeout=30)
            except asyncio.TimeoutError as error:
                logger.error("TimeoutError. URL = %s", url)
                raise HttpTimeoutError(url=url) from error
            except ClientConnectorError as error:
                logger.error("ClientConnectorError. URL = %s", url)
                raise error
            try:
                response.raise_for_status()
            except ClientResponseError as error:
                logger.exception("Error! URL = %s", url)
                if error.status not in self.allow_http_status:
                    raise error
                logger.error("Media may be removed. URL = %s", url)
                return MediaDownloadResult(url, response.status, None)
            try:
                media = await response.read()
            except ClientResponseError as error:
                logger.error("ClientResponseError. URL = %s", url)
                raise HttpTimeoutError(url=url) from error
            media_file = await self.media_save_coroutine.execute(media, download_order.save_order)
            return MediaDownloadResult(url, response.status, media_file)
