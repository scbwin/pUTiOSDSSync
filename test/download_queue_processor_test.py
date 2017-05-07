import unittest
import mock
from mock import Mock, call
from app.download_queue_processor import DownloadQueueProcessor
from app.feed_download_list import FeedDownloadList


class DownloadQueueProcessorTest(unittest.TestCase):

    @mock.patch('feedparser.parse')
    def test_starts_new_downloads(self, mock_feed_parser):
        mock_nas_api = self.setup_nas_with({
            u'total': 0, u'tasks': [], u'offset': 0
        })
        mock_putio_client = Mock()
        processor = DownloadQueueProcessor(mock_nas_api, mock_putio_client)
        urls = [
            u'http://put.io/v2/files/439203060' +
            '/download/podcast.mkv?token=W2PIRV3R',
            u'http://put.io/v2/files/439203063' +
            '/download/podcast.mkv?token=ZLT5JVRP',
        ]
        feed_download = self.setup_feed_with({
            'entries': [{
                'link': urls[0],
                'id': u'http://put.io/file:439203060'
            }, {
                'link': urls[1],
                'id': u'http://put.io/file:439203063'
            }]
        }, mock_feed_parser)

        processor.process(feed_download)

        mock_nas_api.assert_has_calls([
            call.downloadstation.task.request('list', additional='detail'),
            call.downloadstation.task.request('create', uri=urls[0]),
            call.downloadstation.task.request('create', uri=urls[1])
        ])
        assert mock_nas_api.downloadstation.task.request.call_count == 3

    @mock.patch('feedparser.parse')
    def test_does_not_start_running_downloads(self, mock_feed_parser):
        urls = [
            u'http://put.io/v2/files/439203060' +
            '/download/podcast.mkv?token=W2PIRV3R',
            u'http://put.io/v2/files/439203063' +
            '/download/podcast.mkv?token=ZLT5JVRP',
        ]
        mock_nas_api = self.setup_nas_with({
            u'total': 2,
            u'tasks': [{
                u'status': u'downloading',
                u'additional': {
                    u'detail': {
                        u'uri': urls[0],
                    }
                },
                u'id': u'dbid_9862',
            }, {
                u'status': u'waiting',
                u'additional': {
                    u'detail': {
                        u'uri': urls[1],
                    }
                },
                u'id': u'dbid_9863',
            }],
            u'offset': 0
        })
        mock_putio_client = Mock()
        processor = DownloadQueueProcessor(mock_nas_api, mock_putio_client)
        feed_download = self.setup_feed_with({
            'entries': [{
                'link': urls[0],
                'id': u'http://put.io/file:439203060'
            }, {
                'link': urls[1],
                'id': u'http://put.io/file:439203063'
            }]
        }, mock_feed_parser)

        processor.process(feed_download)

        mock_nas_api.assert_has_calls([
            call.downloadstation.task.request('list', additional='detail'),
        ])
        assert mock_nas_api.downloadstation.task.request.call_count == 1

    @mock.patch('feedparser.parse')
    def test_removes_finished_downloads(self, mock_feed_parser):
        urls = [
            u'http://put.io/v2/files/439203060' +
            '/download/podcast.mkv?token=W2PIRV3R',
            u'http://put.io/v2/files/439203063' +
            '/download/podcast.mkv?token=ZLT5JVRP',
        ]
        mock_nas_api = self.setup_nas_with({
            u'total': 2,
            u'tasks': [{
                u'status': u'finished',
                u'additional': {
                    u'detail': {
                        u'uri': urls[0],
                    }
                },
                u'id': u'dbid_9862',
            }, {
                u'status': u'finished',
                u'additional': {
                    u'detail': {
                        u'uri': urls[1],
                    }
                },
                u'id': u'dbid_9863',
            }],
            u'offset': 0
        })
        mock_putio_client = Mock()
        processor = DownloadQueueProcessor(mock_nas_api, mock_putio_client)
        Mock()
        feed_download = self.setup_feed_with({
            'entries': [{
                'link': urls[0],
                'id': u'http://put.io/file:439203060'
            }, {
                'link': urls[1],
                'id': u'http://put.io/file:439203063'
            }]
        }, mock_feed_parser)

        processor.process(feed_download)

        mock_nas_api.assert_has_calls([
            call.downloadstation.task.request('list', additional='detail'),
            call.downloadstation.task.request('delete', id='dbid_9862'),
            call.downloadstation.task.request('delete', id='dbid_9863')
        ])
        assert mock_nas_api.downloadstation.task.request.call_count == 3

    @mock.patch('feedparser.parse')
    def test_removes_files_from_empty_feed(self, mock_feed_parser):
        mock_nas_api = self.setup_nas_with({
            u'total': 0, u'tasks': [], u'offset': 0
        })
        mock_putio_client = Mock()
        mock_putio_feed_file_list = Mock(return_value=[
            Mock(id=433592046),
            Mock(id=433592047)
        ])
        mock_putio_client.File.list = mock_putio_feed_file_list
        mock_putio_client_file = Mock()
        mock_putio_client.File.get = Mock(return_value=mock_putio_client_file)
        processor = DownloadQueueProcessor(mock_nas_api, mock_putio_client)
        feed_download = self.setup_feed_with({
            'entries': []
        }, mock_feed_parser)

        processor.process(feed_download)

        mock_putio_feed_file_list.assert_called_once_with(433592046)
        mock_putio_client.File.get.assert_has_calls([
            call(433592046),
            call(433592047)
        ])
        assert mock_putio_client_file.delete.call_count == 2

    def setup_feed_with(self, feed_download_list, mock_feed_parser):
        mock_feed_parser.return_value = feed_download_list
        feed_url = 'https://username:some_pass@put.io/rss/video/433592046'
        feed_download = FeedDownloadList(feed_url)
        return feed_download

    def setup_nas_with(self, nas_download_list):
        mock_nas_api = Mock()
        mock_nas_api.downloadstation.task.request.side_effect = (
            lambda method, uri=None, additional=None, id=None:
                nas_download_list if method == 'list' else {'status': 'OK'}
        )
        return mock_nas_api
