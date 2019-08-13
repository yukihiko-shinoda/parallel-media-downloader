from datetime import datetime
from typing import List, Tuple

from parallelmediadownloader.media_download_coroutine import DownloadOrder
from parallelmediadownloader.media_file import SaveOrder
from parallelmediadownloader.media_filter import NotImageFilter
from parallelmediadownloader.parallel_media_downloader import ParallelMediaDownloader
from tests.testlibraries.instance_resource import InstanceResource


class TestParallelMediaDownloader:
    @staticmethod
    def test(tmp_path, mock_aioresponse):
        created_date_time1 = datetime(2018, 10, 27, 14, 20, 44)
        created_date_time2 = datetime(2018, 11, 7, 10, 16, 24)
        list_download_order: List[Tuple[DownloadOrder, bytes]] = [
            (DownloadOrder(
                'https://stat.ameba.jp/user_images/20181027/14/da-pump-blog/70/01/j/o1080097814291864857.jpg',
                SaveOrder(
                    tmp_path,
                    '20181027142044stat.ameba.jp_user_images_20181027_14_da-pump-blog_70_01_j_o1080097814291864857.jpg',
                    created_date_time1)),
             InstanceResource.PATH_FILE_IMAGE_97_97_BLUE.read_bytes()),
            (DownloadOrder(
                'https://stat.ameba.jp/user_images/20181027/14/da-pump-blog/6f/ca/j/o1080081014291864864.jpg',
                SaveOrder(
                    tmp_path,
                    '20181027142044stat.ameba.jp_user_images_20181027_14_da-pump-blog_6f_ca_j_o1080081014291864864.jpg',
                    created_date_time1)),
             InstanceResource.PATH_FILE_IMAGE_97_97_GREEN.read_bytes()),
            (DownloadOrder(
                'https://stat.ameba.jp/user_images/20181107/10/da-pump-blog/fe/e6/j/o1080080814298686921.jpg',
                SaveOrder(
                    tmp_path,
                    '20181107101624stat.ameba.jp_user_images_20181107_10_da-pump-blog_fe_e6_j_o1080080814298686921.jpg',
                    created_date_time2)),
             InstanceResource.PATH_FILE_IMAGE_97_97_RED.read_bytes()),
            (DownloadOrder(
                'https://stat.ameba.jp/user_images/20181107/10/da-pump-blog/1d/92/j/o1080080914298686924.jpg',
                SaveOrder(
                    tmp_path,
                    '20181107101624stat.ameba.jp_user_images_20181107_10_da-pump-blog_1d_92_j_o1080080914298686924.jpg',
                    created_date_time2)),
             InstanceResource.PATH_FILE_IMAGE_97_97_YELLOW.read_bytes()),
        ]
        for download_order, byte_data in list_download_order:
            mock_aioresponse.get(download_order.url, status=200, body=byte_data)
        list_media_download_result = ParallelMediaDownloader.execute(
            (download_order for download_order, _ in list_download_order)
        )

        assert len(list_media_download_result) == len(list_download_order)
        for media_download_result, (download_order, content) in zip(list_media_download_result, list_download_order):
            assert media_download_result.url == download_order.url
            assert media_download_result.status == 200
            assert media_download_result.media_file.path_file \
                == download_order.save_order.path_directory_download / download_order.save_order.file_name
            assert media_download_result.media_file.path_file.read_bytes() == content

    @staticmethod
    def test_filter(tmp_path, mock_aioresponse):
        url1 = InstanceResource.URL_TWITTER_IMAGE
        byte1 = InstanceResource.PATH_FILE_IMAGE_TWITTER.read_bytes()
        file_name1 = '20190808154015pbs.twimg.com_media_CeBmNUIUUAAZoQ3'
        list_download_order = [
            DownloadOrder(url1, SaveOrder(tmp_path, file_name1, datetime(2018, 10, 27, 14, 20, 44))),
        ]
        mock_aioresponse.get(url1, status=200, body=byte1)
        list_media_download_result = ParallelMediaDownloader.execute(
            list_download_order, media_filter=NotImageFilter()
        )
        assert len(list_media_download_result) == 1
        media_download_result = list_media_download_result[0]
        assert media_download_result.status == 200
        assert media_download_result.media_file.is_filtered
        assert not media_download_result.media_file.path_file.exists()
