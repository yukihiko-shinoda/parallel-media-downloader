#!/usr/bin/env python
"""This module implements build settings."""

from setuptools import setup
from setuptools import find_packages


def main():
    """This function implements build settings."""
    with open('README.md', 'r', encoding='utf8') as file:
        readme = file.read()

    setup(
        name='parallelmediadownloader',
        version='0.0.1',
        description='This project helps you to download media file.',
        long_description=readme,
        long_description_content_type='text/markdown',
        author='Yukihiko Shinoda',
        author_email='yuk.hik.future@gmail.com',
        packages=find_packages(exclude=("tests*",)),
        package_data={"parallelmediadownloader": ["py.typed"]},
        install_requires=[
            'aiohttp',
        ],
        url="https://github.com/yukihiko-shinoda/parallel-media-downloader",
        keywords="parallel media download downloader image jpg jpeg png gif aiohttp",
    )


if __name__ == '__main__':
    main()
