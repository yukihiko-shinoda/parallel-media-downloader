"""API of parallel media downloading."""
import asyncio
from typing import Iterable, List, Optional

from parallelmediadownloader.media_download_coroutine import DownloadOrder
from parallelmediadownloader.media_filter import MediaFilter
from parallelmediadownloader.modeia_download_result import MediaDownloadResult
from parallelmediadownloader.parallel_media_download_coroutine import ParallelMediaDownloadCoroutine

__all__ = ["ParallelMediaDownloader"]


class ParallelMediaDownloader:
    """API of parallel media downloading."""

    @staticmethod
    def execute(
        list_download_order: Iterable[DownloadOrder],
        *,
        limit: int = 5,
        media_filter: Optional[MediaFilter] = None,
        # Reason: To be this method as non async. pylint: disable=duplicate-code
        allow_http_status: List[int] = None
    ) -> List[MediaDownloadResult]:
        """Executes parallel media downloading."""
        return asyncio.get_event_loop().run_until_complete(
            ParallelMediaDownloadCoroutine.execute(
                list_download_order, limit=limit, media_filter=media_filter, allow_http_status=allow_http_status
            )
        )
