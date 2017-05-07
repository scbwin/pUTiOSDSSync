from download_manager import DownloadManager, DownloadStationCredentials, PutioCredentials, FeedsDetails
import yaml

class Init(object):


    def __init__(self, config_file_location):
        config = yaml.load(file(config_file_location, 'r'))
        synology_config = config['synology']
        self.downloadstation_credentials = DownloadStationCredentials(synology_config['url'], synology_config['username'], synology_config['password'])
        self.putio_credentials = PutioCredentials(config['putio']['token'])
        self.feed_details = FeedsDetails(config['monitor_minutes'], config['feeds'])
        download_manager = DownloadManager(self.downloadstation_credentials, self.putio_credentials, self.feed_details)
