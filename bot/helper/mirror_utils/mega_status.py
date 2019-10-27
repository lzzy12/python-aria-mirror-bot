from bot.helper.ext_utils.bot_utils import get_readable_file_size


class MegaDownloadStatus:
    STATUS_UPLOADING = "Uploading"
    STATUS_DOWNLOADING = "Downloading"
    STATUS_WAITING = "Queued"
    STATUS_FAILED = "Failed. Cleaning download"
    STATUS_CANCELLED = "Cancelled"

    def __init__(self, uid):
        self.uid = uid
        self.name = ''
        self.downloadedBytes = 0
        self.sizeBytes = 0
        self.speed = 0
        self.status = ''

    def name(self) -> str:
        return self.name

    def progress(self):
        """Progress of download in percentage"""
        return (self.downloadedBytes // self.sizeBytes) * 100

    def status(self) -> str:
        return self.status

    def eta(self) -> str:
        return get_readable_file_size(self.sizeBytes / self.speed)

    def size(self) -> str:
        return get_readable_file_size(self.size)

    def downloaded(self) -> str:
        return get_readable_file_size(self.downloadedBytes)

    def speed(self) -> str:
        return f'{get_readable_file_size(self.downloadedBytes)}/s'