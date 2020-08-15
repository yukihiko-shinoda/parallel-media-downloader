#!/usr/bin/env python
"""This module implements build settings."""

from setuptools import find_packages, setup  # type: ignore


def main():
    """This function implements build settings."""
    with open("README.md", "r", encoding="utf8") as file:
        readme = file.read()

    setup(
        author="Yukihiko Shinoda",
        author_email="yuk.hik.future@gmail.com",
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
        dependency_links=[],
        description="This project helps you to download media file.",
        install_requires=["aiohttp"],
        keywords="parallel media download downloader image jpg jpeg png gif aiohttp",
        long_description=readme,
        long_description_content_type="text/markdown",
        name="parallelmediadownloader",
        packages=find_packages(exclude=("tests*",)),
        package_data={"parallelmediadownloader": ["py.typed"]},
        setup_requires=["pytest-runner"],
        url="https://github.com/yukihiko-shinoda/parallel-media-downloader",
        version="0.0.1",
    )


if __name__ == "__main__":
    main()
