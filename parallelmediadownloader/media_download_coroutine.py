# Copyright (C) 2019 Yukihiko Shinoda
"""Coroutine of downloading media."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from logging import getLogger
from typing import TYPE_CHECKING

from aiohttp import ClientConnectorError
from aiohttp import ClientResponseError
from aiohttp import ClientTimeout

from parallelmediadownloader.exceptions import HttpTimeoutError
from parallelmediadownloader.modeia_download_result import MediaDownloadResult

if TYPE_CHECKING:
    from asyncio import Semaphore

    from aiohttp import ClientResponse
    from aiohttp import ClientSession

    from parallelmediadownloader.media_file import SaveOrder
    from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine

__all__ = ["DownloadOrder", "MediaDownloadCoroutine"]

logger = getLogger(__name__)


@dataclass
class DownloadOrder:
    url: str
    save_order: SaveOrder


class MediaDownloadCoroutine:
    """Coroutine of downloading media."""

    # Reason: Based on experience
    TIME_OUT = 30

    def __init__(
        self,
        media_save_coroutine: MediaSaveCoroutine,
        *,
        allow_http_status: list[int] | None = None,
    ) -> None:
        self.media_save_coroutine = media_save_coroutine
        self.allow_http_status = [] if allow_http_status is None else allow_http_status

    async def execute(
        self,
        semaphore: Semaphore,
        client_session: ClientSession,
        download_order: DownloadOrder,
    ) -> MediaDownloadResult:
        """Download media with limiting the number of parallel downloads."""
        url = download_order.url
        async with semaphore:
            response = await self.try_get(client_session, url)
            if self.is_allowed_error(response, url):
                logger.error("Media may be removed. URL = %s", url)
                return MediaDownloadResult(url, response.status, None)
            media = await self.try_read_response(response, url)
            media_file = await self.media_save_coroutine.execute(media, download_order.save_order)
            return MediaDownloadResult(url, response.status, media_file)

    async def try_get(self, client_session: ClientSession, url: str) -> ClientResponse:
        """Try to get request."""
        try:
            return await client_session.get(url, timeout=ClientTimeout(total=self.TIME_OUT))
        except asyncio.TimeoutError as error:
            logger.exception("TimeoutError. URL = %s", url)
            raise HttpTimeoutError(url=url) from error
        except ClientConnectorError:
            logger.exception("ClientConnectorError. URL = %s", url)
            raise

    def is_allowed_error(self, response: ClientResponse, url: str) -> bool:
        """Return whether the response has an HTTP error status which is allowed.

        Raises:
            ClientResponseError: When the response has an HTTP error status which isn't allowed.
        """
        try:
            response.raise_for_status()
        except ClientResponseError as error:
            logger.exception("Error! URL = %s", url)
            if error.status not in self.allow_http_status:
                raise
            return True
        return False

    async def try_read_response(self, response: ClientResponse, url: str) -> bytes:
        try:
            return await response.read()
        except ClientResponseError as error:
            logger.exception("ClientResponseError. URL = %s", url)
            raise HttpTimeoutError(url=url) from error
