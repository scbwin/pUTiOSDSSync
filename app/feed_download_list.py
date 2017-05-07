import feedparser
from download import Download


class FeedDownloadList(object):
    def __init__(self, url):
        self.url = url

    def get_downloads(self):
        return map(lambda x: Download(x['link'], putio_id=self.get_file_id_from_feed_id(x['id'])), feedparser.parse(self.url)['entries'])

    def get_file_id_from_feed_id(self, file_id):
        return int(file_id.rsplit(":", 1)[1])
