from advertising import AbstractRequest, NoArgsRequest


class GetCampaignNegativeKeywordRequest(NoArgsRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.method = "GET"
        self.api = "/v2/sp/campaignNegativeKeywords/%s" % self.keyword_id


class GetCampaignNegativeKeywordExtendedRequest(NoArgsRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.method = "GET"
        self.api = "/v2/sp/campaignNegativeKeywords/extended/%s" % self.keyword_id


class CreateCampaignNegativeKeywordsRequest(AbstractRequest):
    def __init__(self, keywords: list = None):
        super().__init__()
        self.keywords = keywords and keywords or []
        self.api = "/v2/sp/campaignNegativeKeywords"
        self.method = "POST"

    def add_keyword(self, keyword: dict):
        self.keywords.append(keyword)

    def build_args(self):
        return self.keywords


class UpdateCampaignNegativeKeywordsRequest(CreateCampaignNegativeKeywordsRequest):

    def __init__(self, keywords: list = None):
        super().__init__()
        self.keywords = keywords and keywords or []
        self.api = "/v2/sp/campaignNegativeKeywords"
        self.method = "PUT"


class ArchiveCampaignNegativeKeywordRequest(AbstractRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.api = "/v2/sp/campaignNegativeKeywords/%s" % self.keyword_id
        self.method = "DELETE"


class ListCampaignNegativeKeywordsRequest(AbstractRequest):

    def __init__(self,
                 keyword_text: str = None,
                 match_type: list = None,
                 campaign_ids: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):
        super().__init__()
        self.keyword_text = keyword_text
        self.match_type = match_type and match_type or []
        self.campaign_ids = campaign_ids and campaign_ids or []
        self.start_index = start_index
        self.count = count
        self.api = "/v2/sp/campaignNegativeKeywords/"
        self.method = "GET"

    def build_args(self):

        return {
            "startIndex": self.start_index,
            "count": self.count,
            "keywordText": self.keyword_text,
            "matchTypeFilter": ",".join(self.match_type),
            "campaignIdFilter":  ",".join(self.campaign_ids),
        }


class ListCampaignNegativeKeywordsExtendedRequest(ListCampaignNegativeKeywordsRequest):

    def __init__(self,
                 keyword_text: str = None,
                 match_type: list = None,
                 campaign_ids: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):

        super().__init__(keyword_text=keyword_text, match_type=match_type,
                         campaign_ids=campaign_ids,
                         start_index=start_index, count=count)
        self.api = "/v2/sp/campaignNegativeKeywords/extended"
        self.method = "GET"
