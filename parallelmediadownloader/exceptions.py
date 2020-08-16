"""This module implements exceptions for this package."""

__all__ = ["Error", "HttpTimeoutError"]


class Error(Exception):
    """
    Base class for exceptions in this module.
    @see https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """


class HttpTimeoutError(Error):
    def __init__(self, *args, url: str):
        super().__init__(*args)
        self.url = url

    def __str__(self) -> str:
        return f"HttpTimeoutError. URL = {self.url}"
