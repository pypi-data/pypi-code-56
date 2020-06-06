from advertising import AbstractRequest, DownloadRequest, NoArgsRequest

__all__ = ["GetSnapshot", "RequestSnapshot", "DownloadSnapshot"]


class GetSnapshot(NoArgsRequest):

    def __init__(self, snapshot_id: str):
        super().__init__()
        self.snapshot_id = snapshot_id
        self.api = "/v2/sp/snapshots/%s" % self.snapshot_id
        self.method = "GET"


class DownloadSnapshot(DownloadRequest, NoArgsRequest):
    def __init__(self, link: str, dest_file: str = None):
        super().__init__()
        self.api = link
        self.method = "GET"
        self.stream = True
        self.dest_file = dest_file


class RequestSnapshot(AbstractRequest):

    default_state_filters = ["enabled", "paused"]

    def __init__(self, snapshot_type: str, state_filters: list = None):
        super().__init__()
        self.snapshot_type = snapshot_type
        self.state_filters = state_filters and state_filters or self.default_state_filters
        self.api = "/v2/sp/%s/snapshot" % self.snapshot_type
        self.method = "POST"

    def build_args(self):
        return {
            "stateFilter": ",".join(self.state_filters)
        }
