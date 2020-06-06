from advertising import AbstractRequest, NoArgsRequest


class GetAdGroupBidRecommendationsRequest(NoArgsRequest):
    def __init__(self, ad_group_id: str):
        super().__init__()
        self.ad_group_id = ad_group_id
        self.method = "GET"
        self.api = "/v2/sp/adGroups/%s/bidRecommendations" % self.ad_group_id


class GetKeywordBidRecommendationsRequest(NoArgsRequest):
    def __init__(self, keyword_id: str):
        super().__init__()
        self.keyword_id = keyword_id
        self.method = "GET"
        self.api = "/v2/sp/keywords/%s/bidRecommendations" % self.keyword_id


class CreateKeywordBidRecommendationsRequest(AbstractRequest):
    """
    createKeywordBidRecommendations
    POST /v2/sp/ksponsoredeywords/bidRecommendations
    body.txt
    {
    "adGroupId": 264272438240075,
    "keywords": [
        {
        "keyword": "keyword one",
        "matchType": "broad"
        },
        {
        "keyword": "keyword two",
        "matchType": "broad"
        }
    ]
    }
    """

    def __init__(self, keyword_text: str):

        super().__init__()
        self.keyword_text = keyword_text
        self.api = "/v2/sp/sponsoredKeywords/bidRecommendations"
        self.method = "POST"

    def build_args(self):
        return None


class GetBidRecommendationsRequest(AbstractRequest):
    """
    Targeting Bid Recommendations
    getBidRecommendations
    POST  /v2/sp/targets/bidRecommendations
    """

    def __init__(self, ad_group_id: str, expressions: list):
        super().__init__()
        self.ad_group_id = ad_group_id
        self.expressions = expressions
        self.api = "/v2/sp/targets/bidRecommendations"
        self.method = "POST"

    def build_args(self):
        return {
            "adGroupId": self.ad_group_id,
            "expressions": self.expressions
        }
