# Parallel Media Downloader

[![Test](https://github.com/yukihiko-shinoda/parallel-media-downloader/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/parallel-media-downloader/actions?query=workflow%3ATest)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d8aa182721f860764d4d/test_coverage)](https://codeclimate.com/github/yukihiko-shinoda/parallel-media-downloader/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/d8aa182721f860764d4d/maintainability)](https://codeclimate.com/github/yukihiko-shinoda/parallel-media-downloader/maintainability)
[![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/yukihiko-shinoda/parallel-media-downloader)](https://codeclimate.com/github/yukihiko-shinoda/parallel-media-downloader)
[![Updates](https://pyup.io/repos/github/yukihiko-shinoda/parallel-media-downloader/shield.svg)](https://pyup.io/repos/github/yukihiko-shinoda/parallel-media-downloader/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/parallelmediadownloader)](https://pypi.org/project/parallelmediadownloader/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/parallelmediadownloader)](https://pypi.org/project/parallelmediadownloader/)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyukihiko-shinoda%2Fparallel-media-downloader)](http://twitter.com/share?text=Parallel%20Media%20Downloader&url=https://pypi.org/project/parallelmediadownloader/&hashtags=python)

Helps you to download media file in parallel without async / await syntax.

## Feature

This project helps you to download media files in parallel without async / await syntax.

## Installation

```console
pip install parallelmediadownloader
```

## Usage

Minimum example:

```python
from datetime import datetime

from parallelmediadownloader.media_download_coroutine import DownloadOrder
from parallelmediadownloader.media_file import SaveOrder
from parallelmediadownloader.parallel_media_downloader import ParallelMediaDownloader

path_directory_download = "path/directory/download"
created_date_time = datetime.now()
list_download_order = [
    DownloadOrder(
        "https://example.com/test01.png",
        SaveOrder(
            path_directory_download,
            "test01.png",
            created_date_time,
        ),
    ),
    DownloadOrder(
        "https://example.com/test02.png",
        SaveOrder(
            path_directory_download,
            "test02.png",
            created_date_time,
        ),
    ),
    DownloadOrder(
        "https://example.com/test03.png",
        SaveOrder(
            path_directory_download,
            "test03.png",
            created_date_time,
        ),
    ),
]
list_media_download_result = ParallelMediaDownloader.execute(list_download_order)
```

## API

### ParallelMediaDownloader.execute

```python
class ParallelMediaDownloader:
    """API of parallel media downloading."""

    @staticmethod
    def execute(
        list_download_order: Iterable[DownloadOrder],
        *,
        limit: int = 5,
        media_filter: Optional[MediaFilter] = None,
        allow_http_status: List[int] = None
    ) -> List[MediaDownloadResult]:
```

#### list_download_order: Iterable[DownloadOrder]

List of `DownloadOrder`. Method will download them in parallel.

#### limit: int = 5

Limit number of parallel processes.

#### media_filter: Optional[MediaFilter] = None

Filter extends `MediaFilter` to remove downloaded media file depending on file or content of media.
`NotImageFilter` will be help to understand its roll:

```python
class NotImageFilter(MediaFilter):
    def _filter(self, media_file: MediaFile) -> bool:
        return not str(media_file.path_file).lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
```

#### allow_http_status: List[int] = None

By default, ParallelMediaDownloader.execute will check HTTP status code by [Response.raise_for_status](https://requests.readthedocs.io/en/master/_modules/requests/models/#Response.raise_for_status) and whole process will stop.
When HTTP status applies allow_http_status, process will continue.
Then, `MediaDownloadResult.media_file` will be `None`.
