import unittest
import mock
from app.feed_download_list import FeedDownloadList
from app.download import Download


class FeedDownloadListTest(unittest.TestCase):
    @mock.patch('feedparser.parse')
    def test_can_get_downloads_from_feed(self, mock_feed_parser):
        mock_feed_parser.return_value = {
            'entries': [{
                'link': u'http://put.io/v2/files/439203060/download/podcast.mkv?token=ZLT5JVRP',
                'id': u'http://put.io/file:439203060'
            }, {
                'link': u'http://put.io/v2/files/439203063/download/podcast.mkv?token=ZLT5JVRP',
                'id': u'http://put.io/file:439203063'
            }]
        }
        feed_url = 'https://username:some_pass@put.io/rss/video/433592046'
        feed_download = FeedDownloadList(feed_url)

        downloads = feed_download.get_downloads()

        assert len(downloads) == 2
        assert type(downloads[0]) == Download
        assert downloads[0].url == 'http://put.io/v2/files/439203060/download/podcast.mkv?token=ZLT5JVRP'
        assert downloads[1].url == 'http://put.io/v2/files/439203063/download/podcast.mkv?token=ZLT5JVRP'
        assert downloads[0].putio_id == 439203060
        assert downloads[1].putio_id == 439203063
        mock_feed_parser.assert_called_with(feed_url)
