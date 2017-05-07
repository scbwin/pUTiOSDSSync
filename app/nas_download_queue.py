from download import Download

class NasDownloadQueue(object):

    def __init__(self, nas_api):
        self.nas_api = nas_api

    def get_downloads(self):
        return map(lambda x: NasDownloadQueue.to_download(x), self.get_download_tasks_from_nas())

    def get_download_tasks_from_nas(self):
        return self.nas_api.downloadstation.task.request('list', additional='detail')['tasks']

    @staticmethod
    def to_download(x):
        return Download(x['additional']['detail']['uri'], downloadstation_id=x['id'], downloadstation_status=x['status'])

