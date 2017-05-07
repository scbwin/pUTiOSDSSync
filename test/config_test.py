import unittest
import mock
import yaml
from app.config import Init

class InitTest(unittest.TestCase):

    @mock.patch('app.download_manager.NasApi')
    @mock.patch('putio.Client')
    @mock.patch('app.download_manager.BlockingScheduler')
    def test_loads_from_config(self, mock_blocking_scheduler, mock_putio_client, mock_nas_api):
        init = Init('test/config.yml')
        assert init.downloadstation_credentials.url == 'http://localhost:5000'
        assert init.downloadstation_credentials.username == 'admin'
        assert init.downloadstation_credentials.password == 'P@ssw0rd'
        assert init.putio_credentials.token == 'JX12341234'
        assert init.feed_details.refresh_period_in_minutes == 2
        assert len(init.feed_details.feeds_to_monitor) == 2
        assert init.feed_details.feeds_to_monitor[0] == 'https://username:some_pass@put.io/rss/video/433592046'
        assert init.feed_details.feeds_to_monitor[1] == 'https://username:some_pass@put.io/rss/video/433592047'

        mock_nas_api.assert_called_with('http://localhost:5000', 'admin', 'P@ssw0rd')
