import unittest
from mock import Mock
from app.download import Download, UnsupportedOperation


class TestDownload(unittest.TestCase):

    def test_can_create_started_download(self):
        download = self.given_a_download()
        assert download.url == 'http://put.io/v2/files/437243165/download/podcast.mkv?oauth_token=2HXIK7BA'
        assert download.downloadstation_id == 'dbid_9830'
        assert download.status == 'Downloading'

    def test_can_create_finished_download(self):
        download = self.given_a_finished_download()
        assert download.status == 'Finished'

    def test_cant_create_download_without_url(self):
        with self.assertRaises(TypeError):
            Download(downloadstation_id='dbid_9830')

    def test_can_start_download(self):
        nas_api_mock = self.setup_downloadstation_task_response_with({'status': 'OK'})
        download = self.given_a_new_download()

        download.start(nas_api_mock)

        nas_api_mock.downloadstation.task.request.assert_called_with('create', uri=download.url)
        assert download.status == 'Downloading'

    def test_sets_initial_status_to_not_started(self):
        download = self.given_a_new_download()

        assert download.status == 'NotStarted'

    def test_cant_start_finished_download(self):
        nas_api_mock = Mock()
        download = self.given_a_finished_download()

        with self.assertRaises(UnsupportedOperation):
            download.start(nas_api_mock)
        nas_api_mock.downloadstation.task.request.assert_not_called()

    def test_cant_start_arleady_downloading_download(self):
        nas_api_mock = Mock()
        download = self.given_a_download()

        with self.assertRaises(UnsupportedOperation):
            download.start(nas_api_mock)
        nas_api_mock.downloadstation.task.request.assert_not_called()

    def test_can_join_currently_downloading_download_with_same_new_download(self):
        download = self.given_a_new_download()
        same_download = self.given_a_download()

        download.join(same_download)

        assert download.downloadstation_id == 'dbid_9830'
        assert download.status == 'Downloading'

    def test_can_join_finished_downloading_download_with_same_new_download(self):
        download = self.given_a_new_download()
        same_download = self.given_a_finished_download()

        download.join(same_download)

        assert download.status == 'Finished'

    def test_can_join_new_download_with_same_finished_download(self):
        download = self.given_a_finished_download()
        same_download = self.given_a_new_download()

        download.join(same_download)

        assert download.putio_id == 433592046

    def test_cant_join_downloads_that_arent_the_same(self):
        download = self.given_a_new_download()
        other_download = self.given_another_finished_download()

        with self.assertRaises(UnsupportedOperation):
            download.join(other_download)

    def test_can_remove_download(self):
        nas_api_mock = Mock()
        putio_client_mock = Mock()
        putio_client_file = Mock()
        putio_client_mock.File.get = Mock(return_value=putio_client_file)
        download = self.given_a_new_download()
        download.join(self.given_a_finished_download())

        download.remove(nas_api_mock, putio_client_mock)

        nas_api_mock.downloadstation.task.request.assert_called_with('delete', id='dbid_9830')
        putio_client_mock.File.get.assert_called_with(download.putio_id)
        putio_client_file.delete.assert_called_once()

    def test_cant_remove_unfinished_download(self):
        nas_api_mock = Mock()
        putio_client_mock = Mock()
        download = self.given_a_download()

        with self.assertRaises(UnsupportedOperation):
            download.remove(nas_api_mock, putio_client_mock)

        nas_api_mock.downloadstation.task.request.assert_not_called()

    def test_cant_remove_download_without_putio_id(self):
        nas_api_mock = Mock()
        putio_client_mock = Mock()
        download = self.given_a_finished_download()

        with self.assertRaises(UnsupportedOperation):
            download.remove(nas_api_mock, putio_client_mock)

        nas_api_mock.downloadstation.task.request.assert_not_called()

    def given_a_new_download(self):
        return Download('http://put.io/v2/files/437243165/download/podcast.mkv?oauth_token=W2PIRV3R', putio_id=433592046)

    def given_a_download(self):
        return Download('http://put.io/v2/files/437243165/download/podcast.mkv?oauth_token=2HXIK7BA', downloadstation_id='dbid_9830', downloadstation_status='downloading')

    def given_a_finished_download(self):
        return Download('http://put.io/v2/files/437243165/download/podcast.mkv?oauth_token=OKTHRD7F', downloadstation_id='dbid_9830', downloadstation_status=' finished ')

    def given_another_finished_download(self):
        return Download('http://put.io/v2/files/437243167/download/podcast.mkv?oauth_token=LCCATN2H', downloadstation_id='dbid_9831', downloadstation_status='finished')

    def setup_downloadstation_task_response_with(self, return_status):
        nas_api_mock = Mock()
        nas_api_mock.downloadstation.task.request = Mock(return_value=return_status)
        return nas_api_mock
