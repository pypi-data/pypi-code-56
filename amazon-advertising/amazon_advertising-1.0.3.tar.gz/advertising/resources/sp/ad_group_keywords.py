from advertising import AbstractRequest, NoArgsRequest


class GetBiddableKeywordRequest(NoArgsRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.method = "GET"
        self.api = "/v2/sp/keywords/%s" % self.keyword_id


class GetBiddableKeywordExtendedRequest(NoArgsRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.method = "GET"
        self.api = "/v2/sp/keywords/extended/%s" % self.keyword_id


class CreateKeywordsRequest(AbstractRequest):
    def __init__(self, keywrods: list = None):
        super().__init__()
        self.keywords = keywrods and keywrods or []
        self.method = "POST"
        self.api = "/v2/sp/keywords"

    def add_keywrod(self, keyword: dict):
        self.keywords.append(keyword)

    def build_args(self):
        return self.keywords


class UpdateKeywordsRequest(CreateKeywordsRequest):
    def __init__(self, keywrods: list = None):
        super().__init__(keywrods=keywrods)
        self.method = "PUT"


class ArchiveKeywordRequest(NoArgsRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.method = "DELETE"
        self.api = "/v2/sp/keywords/%s" % self.keyword_id


class ListBiddableKeywordsRequest(AbstractRequest):
    def __init__(self,
                 keyword_text: str = None,
                 keyword_ids: list = None,
                 match_type: list = None,
                 states: list = None,
                 campaign_ids: list = None,
                 ad_group_ids: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):
        super().__init__()
        self.keyword_text = keyword_text
        self.match_type = match_type and match_type or []
        self.keyword_ids = keyword_ids and keyword_ids or []
        self.campaign_ids = campaign_ids and campaign_ids or []
        self.ad_group_ids = ad_group_ids and ad_group_ids or []
        self.states = states and states or []
        self.start_index = start_index
        self.count = count
        self.api = "/v2/sp/keywords/"
        self.method = "GET"

    def build_args(self):

        return {
            "startIndex": self.start_index,
            "count": self.count,
            "keywordText": self.keyword_text,
            "matchTypeFilter": ",".join(self.match_type),
            "stateFilter": ",".join(self.states),
            "keywordIdFilter":  ",".join(self.keyword_ids),
            "campaignIdFilter":  ",".join(self.campaign_ids),
            "adGroupIdFilter":  ",".join(self.ad_group_ids),
        }


class ListBiddableKeywordsExtendedRequest(ListBiddableKeywordsRequest):
    def __init__(self,
                 keyword_text: str = None,
                 keyword_ids: list = None,
                 match_type: list = None,
                 states: list = None,
                 campaign_ids: list = None,
                 ad_group_ids: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):
        super().__init__(keyword_text=keyword_text,
                         keyword_ids=keyword_ids,
                         match_type=match_type,
                         states=states,
                         campaign_ids=campaign_ids,
                         ad_group_ids=ad_group_ids,
                         start_index=start_index,
                         count=count)
