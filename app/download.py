class Download(object):
    def __init__(self, url, putio_id=None, downloadstation_id=None, downloadstation_status=None):
        self.putio_id = putio_id
        self.url = url
        self.downloadstation_id = downloadstation_id
        self.status = Download.get_status(downloadstation_id, downloadstation_status)

    def start(self, nas_api):
        self.verify_status_for_start()
        nas_api.downloadstation.task.request('create', uri=self.url)
        self.status = 'Downloading'
        print 'Started download: ', self.url

    def verify_status_for_start(self):
        if self.status != 'NotStarted':
            raise UnsupportedOperation('Can not start a finished download')

    def join(self, other):
        self.verify_status_for_join(other)
        if other.downloadstation_id:
            self.downloadstation_id = other.downloadstation_id
            self.status = other.status
        else:
            self.putio_id = other.putio_id

    def verify_status_for_join(self, other_download):
        if self != other_download:
            raise UnsupportedOperation('Can not join downloads that are not the same')

    def remove(self, nas_api, putio_api):
        self.verify_status_for_stop()
        nas_api.downloadstation.task.request('delete', id=self.downloadstation_id)
        putio_api.File.get(self.putio_id).delete()
        print 'Removed download: ', self.url

    def verify_status_for_stop(self):
        if self.status != 'Finished' or not self.putio_id:
            raise UnsupportedOperation('Can only remove finished downloads')

    def __eq__(self, other):
        return Download.get_url_without_token(self.url) == Download.get_url_without_token(other.url)

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def get_url_without_token(url):
        return url[:url.rfind('?')]

    @staticmethod
    def get_status(downloadstation_id, downloadstation_status):
        status = 'NotStarted'
        if downloadstation_id and downloadstation_status.strip() == 'finished':
            status = 'Finished'
        elif downloadstation_id:
            status = 'Downloading'
        return status


class UnsupportedOperation(Exception):
    pass
