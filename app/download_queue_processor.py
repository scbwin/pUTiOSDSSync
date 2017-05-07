from nas_download_queue import NasDownloadQueue


class DownloadQueueProcessor(object):

    def __init__(self, nas_api, putio_client):
        self.nas_api = nas_api
        self.putio_client = putio_client
        self.nas_download_queue = NasDownloadQueue(nas_api)

    def process(self, feed):
        downloads = feed.get_downloads()
        nas_downloads = self.nas_download_queue.get_downloads()

        if len(downloads) == 0 and len(nas_downloads) == 0:
            [self.cleanup_folder(f) for f in self.putio_client.File.list(int(feed.url.rsplit("/", 1)[1]))]

        else:
            for f in downloads:
                for n in nas_downloads:
                    DownloadQueueProcessor.join_downloads(f, n)
            [d.start(self.nas_api) for d in filter(lambda d: d.status == 'NotStarted', downloads)]
            [d.remove(self.nas_api, self.putio_client) for d in filter(lambda d: d.status == 'Finished', downloads)]

    def cleanup_folder(self, folder):
        print 'Cleaning up ', folder.name, ' folder'
        self.putio_client.File.get(folder.id).delete()

    @staticmethod
    def join_downloads(feed_download, nas_download):
        if feed_download == nas_download:
            feed_download.join(nas_download)
