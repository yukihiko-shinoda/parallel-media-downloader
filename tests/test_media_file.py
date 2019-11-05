import os
from datetime import datetime

from parallelmediadownloader.media_file import MediaFile, SaveOrder
from tests.testlibraries.instance_resource import InstanceResource


class TestSaveOrder:
    @staticmethod
    def test(tmp_path):
        file_name = '20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3'
        save_order = SaveOrder(tmp_path, file_name, datetime(2019, 8, 8, 15, 40, 15))
        assert save_order.path_file == tmp_path / file_name


class TestMediaFile:
    @staticmethod
    def test(tmp_path):
        file_name = 'test.PNG'
        created_date_time = datetime(2019, 8, 8, 2, 28, 15)
        file_path = tmp_path / file_name
        save_order = SaveOrder(tmp_path, file_name, created_date_time)
        media_file = MediaFile(InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes(), save_order)
        assert os.path.getatime(str(file_path)) == created_date_time.timestamp()
        assert os.path.getmtime(str(file_path)) == created_date_time.timestamp()
        assert file_path.read_bytes() == InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes()
        assert media_file.is_filtered is None
        media_file.remove()
        assert not file_path.exists()
