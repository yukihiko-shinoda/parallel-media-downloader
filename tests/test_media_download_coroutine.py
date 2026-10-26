# Copyright (C) 2019 Yukihiko Shinoda
"""Test for media_download_coroutine."""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from typing import TYPE_CHECKING

import aiohttp
import pytest
from aiohttp import ClientConnectorError
from aiohttp import ClientResponse
from aiohttp import ClientResponseError
from aiohttp import RequestInfo
from aioresponses import CallbackResult
from multidict import CIMultiDict
from multidict import CIMultiDictProxy
from yarl import URL

from parallelmediadownloader.exceptions import HttpTimeoutError
from parallelmediadownloader.media_download_coroutine import MediaDownloadCoroutine
from parallelmediadownloader.media_save_coroutine import MediaSaveCoroutine
from tests.testlibraries.instance_resource import InstanceResource

if TYPE_CHECKING:
    from aioresponses import aioresponses
    from pytest_mock import MockerFixture

    from parallelmediadownloader.media_download_coroutine import DownloadOrder


class MockClientResponse(ClientResponse):
    async def read(self) -> bytes:
        raise ClientResponseError(RequestInfo(URL(), "", CIMultiDictProxy(CIMultiDict())), ())


def callback_mock_client_response(_url: URL, **_kwargs: object) -> CallbackResult:
    return CallbackResult(response_class=MockClientResponse)


class TestMediaDownloadCoroutine:
    """Test for MediaDownloadCoroutine."""

    @staticmethod
    @pytest.mark.asyncio
    async def test(
        mock_aioresponse: aioresponses,
        bytes_image_twitter: bytes,
        download_order: DownloadOrder,
    ) -> None:
        """Tests."""
        mock_aioresponse.get(InstanceResource.URL_TWITTER_IMAGE, status=HTTPStatus.OK, body=bytes_image_twitter)
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as client_session:
            media_download_result = await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(
                semaphore,
                client_session,
                download_order,
            )
        assert media_download_result.url == "https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium"
        assert media_download_result.status == HTTPStatus.OK
        assert media_download_result.media_file is not None
        path_file = media_download_result.media_file.path_file
        assert path_file == download_order.save_order.path_file
        assert path_file.read_bytes() == bytes_image_twitter

    @staticmethod
    @pytest.mark.asyncio
    async def test_timeout_error(mock_aioresponse: aioresponses, download_order: DownloadOrder) -> None:
        """Tests HttpTimeoutError."""
        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE,
            status=HTTPStatus.OK,
            exception=asyncio.TimeoutError(),
        )
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as client_session:
            with pytest.raises(HttpTimeoutError) as error:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert str(error.value) == (
            "HttpTimeoutError. URL = https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium"
        )

    @staticmethod
    @pytest.mark.asyncio
    async def test_client_connector_error(
        mocker: MockerFixture,
        mock_aioresponse: aioresponses,
        download_order: DownloadOrder,
    ) -> None:
        """Tests ClientConnectorError."""
        mock = mocker.Mock()
        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE,
            status=HTTPStatus.OK,
            exception=ClientConnectorError(mock, OSError()),
        )
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as client_session:
            with pytest.raises(ClientConnectorError) as error:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert "Cannot connect to host" in str(error.value)

    @staticmethod
    @pytest.mark.asyncio
    async def test_allow_http_status_success(
        mock_aioresponse: aioresponses,
        bytes_image_twitter: bytes,
        download_order: DownloadOrder,
    ) -> None:
        """Tests allow_http_status in case of success."""
        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE,
            status=HTTPStatus.NOT_FOUND,
            body=bytes_image_twitter,
        )
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as client_session:
            media_download_result = await MediaDownloadCoroutine(
                MediaSaveCoroutine(),
                allow_http_status=[HTTPStatus.NOT_FOUND],
            ).execute(semaphore, client_session, download_order)
        assert media_download_result.url == "https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium"
        assert media_download_result.status == HTTPStatus.NOT_FOUND
        assert media_download_result.media_file is None

    @staticmethod
    @pytest.mark.asyncio
    async def test_allow_http_status_error(
        mock_aioresponse: aioresponses,
        bytes_image_twitter: bytes,
        download_order: DownloadOrder,
    ) -> None:
        """Tests allow_http_status in case of error."""
        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE,
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            body=bytes_image_twitter,
        )
        semaphore = asyncio.Semaphore(5)
        media_download_coroutine = MediaDownloadCoroutine(
            MediaSaveCoroutine(),
            allow_http_status=[HTTPStatus.NOT_FOUND],
        )
        async with aiohttp.ClientSession() as client_session:
            with pytest.raises(ClientResponseError) as error:
                await media_download_coroutine.execute(semaphore, client_session, download_order)
        assert "Internal Server Error" in str(error.value)

    @staticmethod
    @pytest.mark.asyncio
    async def test_client_response_error_when_read(
        mock_aioresponse: aioresponses,
        download_order: DownloadOrder,
    ) -> None:
        """Tests ClientResponseError when read."""
        mock_aioresponse.get(
            InstanceResource.URL_TWITTER_IMAGE,
            status=HTTPStatus.OK,
            callback=callback_mock_client_response,
        )
        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession() as client_session:
            with pytest.raises(HttpTimeoutError) as error:
                await MediaDownloadCoroutine(MediaSaveCoroutine()).execute(semaphore, client_session, download_order)
        assert str(error.value) == (
            "HttpTimeoutError. URL = https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium"
        )
