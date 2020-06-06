from advertising import AbstractRequest, NoArgsRequest


class GetNegativeKeywordRequest(NoArgsRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.method = "GET"
        self.api = "/v2/sp/negativeKeywords/%s" % self.keyword_id


class GetNegativeKeywordExtendedRequest(NoArgsRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.method = "GET"
        self.api = "/v2/sp/negativeKeywords/extended/%s" % self.keyword_id


class CreateNegativeKeywordsRequest(AbstractRequest):
    def __init__(self, keywords: list = None):
        super().__init__()
        self.keywords = keywords and keywords or []
        self.api = "/v2/sp/negativeKeywords"
        self.method = "POST"

    def add_keyword(self, keyword: dict):
        self.keywords.append(keyword)

    def build_args(self):
        return self.keywords


class UpdateNegativeKeywordsRequest(CreateNegativeKeywordsRequest):

    def __init__(self, keywords: list = None):
        super().__init__()
        self.keywords = keywords and keywords or []
        self.api = "/v2/sp/negativeKeywords"
        self.method = "PUT"


class ArchiveNegativeKeywordRequest(AbstractRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.api = "/v2/sp/negativeKeywords/%s" % self.keyword_id
        self.method = "DELETE"


class ListNegativeKeywordsRequest(AbstractRequest):

    def __init__(self,
                 keyword_text: str = None,
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
        self.campaign_ids = campaign_ids and campaign_ids or []
        self.ad_group_ids = ad_group_ids and ad_group_ids or []
        self.states = states and states or []
        self.start_index = start_index
        self.count = count
        self.api = "/v2/sp/negativeKeywords/"
        self.method = "GET"

    def build_args(self):

        return {
            "startIndex": self.start_index,
            "count": self.count,
            "keywordText": self.keyword_text,
            "matchTypeFilter": ",".join(self.match_type),
            "stateFilter": ",".join(self.states),
            "campaignIdFilter":  ",".join(self.campaign_ids),
            "adGroupIdFilter":  ",".join(self.ad_group_ids),
        }


class ListNegativeKeywordsExtendedRequest(ListNegativeKeywordsRequest):
    def __init__(self,
                 keyword_text: str = None,
                 match_type: list = None,
                 states: list = None,
                 campaign_ids: list = None,
                 ad_group_ids: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):

        super().__init__(keyword_text=keyword_text, match_type=match_type, states=states,
                         campaign_ids=campaign_ids, ad_group_ids=ad_group_ids,
                         start_index=start_index, count=count)
        self.api = "/v2/sp/negativeKeywords/extended"
        self.method = "GET"
