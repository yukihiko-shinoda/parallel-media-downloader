from pathlib import Path


class InstanceResource:
    """This class implements fixture of instance."""
    PATH_TESTS: Path = Path(__file__).parent.parent
    PATH_TEST_RESOURCES: Path = PATH_TESTS / 'testresources'
    PATH_FILE_IMAGE_97_97_BLUE: Path = PATH_TEST_RESOURCES / '97x97_blue.png'
    PATH_FILE_IMAGE_97_97_GREEN: Path = PATH_TEST_RESOURCES / '97x97_green.png'
    PATH_FILE_IMAGE_97_97_RED: Path = PATH_TEST_RESOURCES / '97x97_red.png'
    PATH_FILE_IMAGE_97_97_YELLOW: Path = PATH_TEST_RESOURCES / '97x97_yellow.png'
    PATH_FILE_IMAGE_TWITTER: Path = PATH_TEST_RESOURCES / 'image_twitter.jpg'
    URL_TWITTER_IMAGE = 'https://pbs.twimg.com/media/CeBmNUIUUAAZoQ3?format=jpg&name=medium'
