#!/usr/bin/env python
"""This module implements build settings."""

from setuptools import setup
from setuptools import find_packages


def main():
    """This function implements build settings."""
    with open("README.md", "r", encoding="utf8") as file:
        readme = file.read()

    setup(
        name="parallelmediadownloader",
        version="0.0.1",
        description="This project helps you to download media file.",
        long_description=readme,
        long_description_content_type="text/markdown",
        author="Yukihiko Shinoda",
        author_email="yuk.hik.future@gmail.com",
        packages=find_packages(exclude=("tests*",)),
        package_data={"parallelmediadownloader": ["py.typed"]},
        install_requires=["aiohttp"],
        dependency_links=[],
        url="https://github.com/yukihiko-shinoda/parallel-media-downloader",
        keywords="parallel media download downloader image jpg jpeg png gif aiohttp",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Multimedia :: Graphics",
            "Topic :: System :: Archiving",
            "Topic :: System :: Archiving :: Backup",
            "Typing :: Typed",
        ],
    )


if __name__ == "__main__":
    main()
