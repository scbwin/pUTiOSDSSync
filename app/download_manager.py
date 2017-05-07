from synolopy import NasApi
import putio
from download_queue_processor import DownloadQueueProcessor
from feed_download_list import FeedDownloadList
from apscheduler.schedulers.blocking import BlockingScheduler
import logging


class DownloadManager:

    def __init__(self, downloadstation_credentials, putio_credentials, feeds_details):
        nas_api = NasApi(downloadstation_credentials.url, downloadstation_credentials.username, downloadstation_credentials.password)
        putio_client = putio.Client(putio_credentials.token)
        self.download_queue_processor = DownloadQueueProcessor(nas_api, putio_client)
        self.feeds_details = feeds_details
        logging.basicConfig()
        self.scheduler = BlockingScheduler()
        self.scheduler.add_job(self.process_feeds, 'interval', minutes=feeds_details.refresh_period_in_minutes)
        self.scheduler.start()

    def process_feeds(self):
        print 'Starting processing of feeds'
        [self.download_queue_processor.process(FeedDownloadList(f)) for f in self.feeds_details.feeds_to_monitor]
        print 'Finished processing feeds'


class DownloadStationCredentials(object):

    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password


class PutioCredentials(object):

    def __init__(self, token):
        self.token = token


class FeedsDetails(object):

    def __init__(self, refresh_period_in_minutes, feeds_to_monitor):
        self.refresh_period_in_minutes = refresh_period_in_minutes
        self.feeds_to_monitor = feeds_to_monitor
