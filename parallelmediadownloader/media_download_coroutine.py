import asyncio
from asyncio import Semaphore
from dataclasses import dataclass

from aiohttp import ClientSession, ClientConnectorError, ClientResponseError

from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine, SaveOrder
from parallelmediadownloader.exceptions import HttpTimeoutError
from parallelmediadownloader.modeia_download_result import MediaDownloadResult


@dataclass
class DownloadOrder:
    url: str
    save_order: SaveOrder


class MediaDownloadCoroutine:
    def __init__(self, media_save_coroutine: MediaSaveCoroutine):
        self.media_save_coroutine = media_save_coroutine

    async def execute(
            self, semaphore: Semaphore, client_session: ClientSession, download_order: DownloadOrder
    ) -> MediaDownloadResult:
        """function want to limit the number of parallel"""
        url = download_order.url
        async with semaphore:
            try:
                response = await client_session.get(url, timeout=30)
            except asyncio.TimeoutError as error:
                print(url)
                raise HttpTimeoutError(url=url) from error
            except ClientConnectorError as error:
                print(f'ClientConnectorError. URL = {url}')
                raise error
            response.raise_for_status()
            try:
                media = await response.read()
            except ClientResponseError as error:
                print(url)
                raise HttpTimeoutError(url=url) from error
            media_file = await self.media_save_coroutine.execute(media, download_order.save_order)
            return MediaDownloadResult(url, response.status, media_file)
