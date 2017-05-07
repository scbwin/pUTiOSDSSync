import unittest
from mock import Mock
from app.nas_download_queue import NasDownloadQueue
from app.download import Download

class NasDownloadQueueTest(unittest.TestCase):

    def test_can_get_downloads_from_nas(self):
        mock_nas_api = Mock()
        mock_nas_api.downloadstation.task.request.return_value = {
            u'total': 3,
            u'tasks': [{
                u'status': u'finished',
                u'additional': {
                    u'detail': {
                        u'uri': u'http://put.io/v2/files/439401574/download/podcast.mkv?token=ZLT5JVRP',
                    }
                },
                u'id': u'dbid_9862',
            }, {
                u'status': u'finished',
                u'additional': {
                    u'detail': {
                        u'uri': u'http://put.io/v2/files/439364195/download/podcast.mkv?token=ZLT5JVRP',
                    }
                },
                u'id': u'dbid_9863',
            }, {
                u'status': u'downloading',
                u'username': u'admin',
                u'additional': {
                    u'detail': {
                        u'uri': u'http://put.io/v2/files/439203060/download/podcast.mkv?token=ZLT5JVRP',
                    }
                },
                u'id': u'dbid_9861',
            }],
            u'offset': 0
        }
        nas_download_queue = NasDownloadQueue(mock_nas_api)

        downloads = nas_download_queue.get_downloads()

        mock_nas_api.downloadstation.task.request.assert_called_with('list', additional='detail')
        assert len(downloads) == 3
        assert type(downloads[0]) == Download
        assert downloads[0].url == 'http://put.io/v2/files/439401574/download/podcast.mkv?token=ZLT5JVRP'
        assert downloads[0].downloadstation_id == 'dbid_9862'
        assert downloads[0].status == 'Finished'
        assert downloads[2].status == 'Downloading'

