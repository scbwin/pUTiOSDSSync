import unittest
import mock
from mock import call
from app.download_manager import DownloadManager, DownloadStationCredentials, PutioCredentials, FeedsDetails


class DownloadManagerTest(unittest.TestCase):

    @mock.patch('app.download_manager.NasApi')
    @mock.patch('putio.Client')
    @mock.patch('app.download_manager.BlockingScheduler')
    def test_can_create_download_manager(self, mock_blocking_scheduler, mock_putio_client, mock_nas_api):
        self.given_a_download_manager()

        mock_nas_api.assert_called_with('some_url', 'admin', 'some password')
        mock_putio_client.assert_called_with('JXXXXXXl')

    @mock.patch('app.download_manager.NasApi')
    @mock.patch('putio.Client')
    @mock.patch('app.download_manager.BlockingScheduler')
    def test_schedules_processing_of_feeds(self, mock_blocking_scheduler, mock_putio_client, mock_nas_api):
        download_manager = self.given_a_download_manager()

        download_manager.scheduler.add_job.assert_called_with(download_manager.process_feeds, 'interval', minutes=1)
        download_manager.scheduler.start.assert_called_once()

    @mock.patch('app.download_manager.NasApi')
    @mock.patch('putio.Client')
    @mock.patch('app.download_manager.BlockingScheduler')
    @mock.patch('feedparser.parse')
    def test_process_feeds_processes_all_feeds(self, mock_feedparser, mock_blocking_scheduler, mock_putio_client, mock_nas_api):
        download_manager = self.given_a_download_manager()

        download_manager.process_feeds()

        mock_feedparser.assert_has_calls([
            call('https://username:some_pass@put.io/rss/video/433592046'),
            call('https://username:some_pass@put.io/rss/video/433592047')
        ], any_order=True)

    def given_a_download_manager(self):
        downloadstation_credentials = DownloadStationCredentials('some_url', 'admin', 'some password')
        putio_credentials = PutioCredentials('JXXXXXXl')
        feeds_details = FeedsDetails(1, ['https://username:some_pass@put.io/rss/video/433592046', 'https://username:some_pass@put.io/rss/video/433592047'])
        return DownloadManager(downloadstation_credentials, putio_credentials, feeds_details)
