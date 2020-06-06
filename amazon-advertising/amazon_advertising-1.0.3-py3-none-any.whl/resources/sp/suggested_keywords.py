from advertising import AbstractRequest, NoArgsRequest

__all__ = ["GetAdGroupSuggestedKeywords",
           "GetAdGroupSuggestedKeywordsExtended", "BulkAsinSuggestedKeywords"]


class GetAdGroupSuggestedKeywords(NoArgsRequest):

    def __init__(self, ad_group_id: str):
        super().__init__()
        self.ad_group_id = ad_group_id
        self.api = "/v2/sp/adGroups/%s/suggested/keywords" % self.ad_group_id
        self.method = "GET"


class GetAdGroupSuggestedKeywordsExtended(NoArgsRequest):

    def __init__(self, ad_group_id: str):
        super().__init__()
        self.ad_group_id = ad_group_id
        self.api = "/v2/sp/adGroups/%s/suggested/keywords/extended" % self.ad_group_id
        self.method = "GET"


class BulkAsinSuggestedKeywords(AbstractRequest):

    def __init__(self, asins: list, max_num_suggestion: int = 100):
        super().__init__()
        self.asins = asins
        self.max_num_suggestion = max_num_suggestion
        self.api = "/v2/sp/asins/suggested/keywords"
        self.method = "POST"

    def build_args(self):
        return {
            "asins": self.asins,
            "maxNumSuggestions": self.max_num_suggestion
        }
