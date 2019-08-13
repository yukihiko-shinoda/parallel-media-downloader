import asyncio
from datetime import datetime

import aiohttp
from aiohttp import ClientResponseError, RequestInfo, ClientResponse, ClientConnectorError
from aioresponses import CallbackResult
from multidict import CIMultiDictProxy, CIMultiDict
import pytest

from parallelmediadownloader.exceptions import HttpTimeoutError
from parallelmediadownloader.media_file import SaveOrder
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine
from parallelmediadownloader.media_download_coroutine import MediaDownloadCoroutine, DownloadOrder
from tests.testlibraries.instance_resource import InstanceResource


class TestMediaDownloadCoroutine:
    @staticmethod
    @pytest.mark.asyncio
    async def test(mock_aioresponse, tmp_path):
        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE, status=200, body=InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes()
        )
        file_name = '20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3'
        created_date_time = datetime(2019, 8, 8, 15, 40, 15)
        download_order = DownloadOrder(
            InstanceResource.URL_TWITTER_IMAGE, SaveOrder(tmp_path, file_name, created_date_time)
        )
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as client_session:
            media_download_result = await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(
                semaphore, client_session, download_order
            )
        assert media_download_result.url == 'https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium'
        assert media_download_result.status == 200
        path_file = media_download_result.media_file.path_file
        assert path_file == (tmp_path / file_name)
        assert path_file.read_bytes() == InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes()

    @staticmethod
    @pytest.mark.asyncio
    async def test_timeout_error(mock_aioresponse, tmp_path):
        mock_aioresponse.get(InstanceResource.URL_TWITTER_IMAGE, status=200, exception=asyncio.TimeoutError())
        file_name = '20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3'
        created_date_time = datetime(2019, 8, 8, 15, 40, 15)
        download_order = DownloadOrder(
            InstanceResource.URL_TWITTER_IMAGE, SaveOrder(tmp_path, file_name, created_date_time)
        )
        with pytest.raises(HttpTimeoutError) as error:
            semaphore = asyncio.Semaphore(5)
            async with aiohttp.ClientSession() as client_session:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert str(error.value) == ('HttpTimeoutError. URL = '
                                    'https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium')

    @staticmethod
    @pytest.mark.asyncio
    async def test_client_connector_error(mocker, mock_aioresponse, tmp_path):
        mock = mocker.Mock()
        mock_aioresponse.get(InstanceResource.URL_TWITTER_IMAGE, status=200, exception=ClientConnectorError(
            mock, OSError()
        ))
        file_name = '20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3'
        created_date_time = datetime(2019, 8, 8, 15, 40, 15)
        download_order = DownloadOrder(
            InstanceResource.URL_TWITTER_IMAGE, SaveOrder(tmp_path, file_name, created_date_time)
        )
        with pytest.raises(ClientConnectorError) as error:
            semaphore = asyncio.Semaphore(5)
            async with aiohttp.ClientSession() as client_session:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert 'Cannot connect to host' in str(error.value)

    @staticmethod
    @pytest.mark.asyncio
    async def test_client_response_error(mock_aioresponse, tmp_path):
        class MockClientResponse(ClientResponse):
            async def read(self):
                raise ClientResponseError(RequestInfo('', '', CIMultiDictProxy(CIMultiDict()), ''), ())
        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE,
            status=200,
            callback=lambda url, **kwargs: CallbackResult(response_class=MockClientResponse)  # noqa
            # Reason: AioResponse's bug.
        )
        file_name = '20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3'
        created_date_time = datetime(2019, 8, 8, 15, 40, 15)
        download_order = DownloadOrder(
            InstanceResource.URL_TWITTER_IMAGE, SaveOrder(tmp_path, file_name, created_date_time)
        )
        with pytest.raises(HttpTimeoutError) as error:
            semaphore = asyncio.Semaphore(5)
            async with aiohttp.ClientSession() as client_session:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert str(error.value) == ('HttpTimeoutError. URL = '
                                    'https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium')
