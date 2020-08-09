"""Test for media_download_coroutine."""
import asyncio
from datetime import datetime

import aiohttp
import pytest
from aiohttp import ClientConnectorError, ClientResponse, ClientResponseError, RequestInfo
from aioresponses import CallbackResult  # type: ignore
from multidict import CIMultiDict, CIMultiDictProxy

from parallelmediadownloader.exceptions import HttpTimeoutError
from parallelmediadownloader.media_download_coroutine import DownloadOrder, MediaDownloadCoroutine
from parallelmediadownloader.media_file import SaveOrder
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine
from tests.testlibraries.instance_resource import InstanceResource


@pytest.fixture
def download_order(tmp_path):
    yield DownloadOrder(
        InstanceResource.URL_TWITTER_IMAGE,
        SaveOrder(tmp_path, "20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3", datetime(2019, 8, 8, 15, 40, 15)),
    )


class TestMediaDownloadCoroutine:
    """Test for MediaDownloadCoroutine."""

    # pylint: disable=redefined-outer-name
    @staticmethod
    @pytest.mark.asyncio
    async def test(mock_aioresponse, bytes_image_twitter, download_order):
        """Tests."""
        mock_aioresponse.get(InstanceResource.URL_TWITTER_IMAGE, status=200, body=bytes_image_twitter)
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as client_session:
            media_download_result = await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(
                semaphore, client_session, download_order
            )
        assert media_download_result.url == "https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium"
        assert media_download_result.status == 200
        path_file = media_download_result.media_file.path_file
        assert path_file == download_order.save_order.path_file
        assert path_file.read_bytes() == bytes_image_twitter

    # pylint: disable=redefined-outer-name
    @staticmethod
    @pytest.mark.asyncio
    async def test_timeout_error(mock_aioresponse, download_order):
        """Tests HttpTimeoutError."""
        mock_aioresponse.get(InstanceResource.URL_TWITTER_IMAGE, status=200, exception=asyncio.TimeoutError())
        with pytest.raises(HttpTimeoutError) as error:
            semaphore = asyncio.Semaphore(5)
            async with aiohttp.ClientSession() as client_session:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert str(error.value) == (
            "HttpTimeoutError. URL = " "https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium"
        )

    # pylint: disable=redefined-outer-name
    @staticmethod
    @pytest.mark.asyncio
    async def test_client_connector_error(mocker, mock_aioresponse, download_order):
        """Tests ClientConnectorError."""
        mock = mocker.Mock()
        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE, status=200, exception=ClientConnectorError(mock, OSError())
        )
        with pytest.raises(ClientConnectorError) as error:
            semaphore = asyncio.Semaphore(5)
            async with aiohttp.ClientSession() as client_session:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert "Cannot connect to host" in str(error.value)

    # pylint: disable=redefined-outer-name
    @staticmethod
    @pytest.mark.asyncio
    async def test_allow_http_status_success(mock_aioresponse, bytes_image_twitter, download_order):
        """Tests allow_http_status in case of success."""
        mock_aioresponse.get(InstanceResource.URL_TWITTER_IMAGE, status=404, body=bytes_image_twitter)
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as client_session:
            media_download_result = await MediaDownloadCoroutine(MediaSaveCoroutine(), allow_http_status=[404]).execute(
                semaphore, client_session, download_order
            )
        assert media_download_result.url == "https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium"
        assert media_download_result.status == 404
        assert media_download_result.media_file is None

    # pylint: disable=redefined-outer-name
    @staticmethod
    @pytest.mark.asyncio
    async def test_allow_http_status_error(mock_aioresponse, bytes_image_twitter, download_order):
        """Tests allow_http_status in case of error."""
        mock_aioresponse.get(InstanceResource.URL_TWITTER_IMAGE, status=500, body=bytes_image_twitter)
        with pytest.raises(ClientResponseError) as error:
            semaphore = asyncio.Semaphore(5)
            async with aiohttp.ClientSession() as client_session:
                await MediaDownloadCoroutine(MediaSaveCoroutine(), allow_http_status=[404]).execute(
                    semaphore, client_session, download_order
                )
        assert "Internal Server Error" in str(error.value)

    # pylint: disable=redefined-outer-name
    @staticmethod
    @pytest.mark.asyncio
    async def test_client_response_error_when_read(mock_aioresponse, download_order):
        """Tests ClientResponseError when read."""

        class MockClientResponse(ClientResponse):
            async def read(self):
                raise ClientResponseError(RequestInfo("", "", CIMultiDictProxy(CIMultiDict()), ""), ())

        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE,
            status=200,
            callback=lambda url, **kwargs: CallbackResult(response_class=MockClientResponse)  # noqa
            # Reason: AioResponse's bug.
        )
        with pytest.raises(HttpTimeoutError) as error:
            semaphore = asyncio.Semaphore(5)
            async with aiohttp.ClientSession() as client_session:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert str(error.value) == (
            "HttpTimeoutError. URL = " "https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium"
        )
