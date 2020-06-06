from advertising import AbstractRequest, NoArgsRequest

__all__ = ["GetTargetingRequest", "GetTargetingExtendedRequest", "ListTargetingRequest",
           "ListTargetingExtendedRequest", "ListTargetingExtendedRequest", "CreateTargetingRequest",
           "CreateTargetingRecommendations", "UpdateTargetingRequest", "ArchiveTargetingRequest", "GetTargetingCategoriesRequest",
           "GetTargetingCategoriesRefinementsRequest", "GetBrandRecommendationsRequest", "GetNegativeTargetingRequest", "GetNegativeTargetingExtendedRequest",
           "ListNegativeTargetingRequest", "ListNegativeTargetingExtendedRequest", "CreateNegativeTargetingRequest", "ArchiveNegativeTargetingRequest", "UpdateNegativeTargetingRequest"
           ]


class GetTargetingRequest(NoArgsRequest):
    def __init__(self, target_id: str):
        super().__init__()
        self.target_id = target_id
        self.api = "/v2/sp/targets/%s" % self.target_id
        self.method = "GET"


class GetTargetingExtendedRequest(GetTargetingRequest):
    def __init__(self, target_id: str):
        super().__init__(target_id)
        self.api = "/v2/sp/targets/extended/%s" % self.target_id


class ListTargetingRequest(AbstractRequest):
    def __init__(self, target_ids: list = None, campaign_ids: list = None, ad_group_ids: list = None, states: list = None, category_id: str = None, start_index: int = 0, count: int = 100):
        super().__init__()
        self.target_ids = target_ids and target_ids or []
        self.campaign_ids = campaign_ids and campaign_ids or []
        self.ad_group_ids = ad_group_ids and ad_group_ids or []
        self.states = states and states or []
        self.start_index = start_index
        self.category_id = category_id
        self.count = count
        self.api = "/v2/sp/targets"
        self.method = "GET"

    def build_args(self):

        return {
            "startIndex": self.start_index,
            "count": self.count,
            "stateFilter": ",".join(self.states),
            "campaignIdFilter":  ",".join(self.campaign_ids),
            "adGroupIdFilter":  ",".join(self.ad_group_ids),
            "targetIdFilter": ",".join(self.target_ids),
            "categoryId": self.category_id
        }


class ListTargetingExtendedRequest(ListTargetingRequest):

    def __init__(self, target_ids: list = None, campaign_ids: list = None, ad_group_ids: list = None, states: list = None, start_index: int = 0, count: int = 100):
        super().__init__(target_ids=target_ids, campaign_ids=campaign_ids,
                         ad_group_ids=ad_group_ids, states=states, start_index=start_index, count=count)
        self.api = "/v2/sp/targets/extended"


class CreateTargetingRequest(AbstractRequest):
    def __init__(self, targetings: list = None):
        super.__init__()
        self.targetings = targetings and targetings or []
        self.api = "/v2/sp/targets/"
        self.method = "POST"

    def add_targeting(self, targeting:dict):
        self.targetings.append(targeting)

    def build_args(self):
        return self.targetings


class CreateTargetingRecommendations(AbstractRequest):
    def __init__(self, recommendations: list = None):
        super.__init__()
        self.recommendations = recommendations and recommendations or []
        self.api = "/v2/sp/targets/productRecommendations"
        self.method = "POST"

    def add_recommendation(self, recommendation:dict):
        self.recommendations.append(recommendation)

    def build_args(self):
        return self.recommendations


class UpdateTargetingRequest(CreateTargetingRequest):
    def __init__(self, targetings: list = None):
        super.__init__(targetings)
        self.method = "PUT"


class ArchiveTargetingRequest(CreateTargetingRequest):
    def __init__(self, targetings: list = None):
        super.__init__(targetings)
        self.method = "DELETE"


class GetTargetingCategoriesRequest(AbstractRequest):
    def __init__(self, asins: list = None):
        super.__init__()
        self.api = "/v2/sp/targets/categories"
        self.method = "GET"
        self.asins = asins and asins or []

    def build_args(self):
        return {
            "asins": ",".join(self.asins)
        }


class GetTargetingCategoriesRefinementsRequest(AbstractRequest):
    def __init__(self, category_id: int = None):
        super.__init__()
        self.api = "/v2/sp/targets/categories/refinements"
        self.method = "GET"
        self.category_id = category_id

    def build_args(self):
        return {
            "categoryId":  self.category_id
        }


class GetBrandRecommendationsRequest(AbstractRequest):
    def __init__(self, keyword: str = None, category_id: int = None):
        super.__init__()
        self.api = "/v2/sp/targets/brands"
        self.method = "GET"
        self.keyword = keyword
        self.category_id = category_id

    def build_args(self):
        return {
            "keyword": self.keyword,
            "categoryId":  self.category_id
        }


class GetNegativeTargetingRequest(NoArgsRequest):
    def __init__(self, target_id: str = None):
        super.__init__()
        self.target_id = target_id
        self.api = "/v2/sp/negativeTargets/%s" % self.target_id
        self.method = "GET"


class GetNegativeTargetingExtendedRequest(NoArgsRequest):
    def __init__(self, target_id: str = None):
        super.__init__()
        self.target_id = target_id
        self.api = "/v2/sp/negativeTargets/extended/%s" % self.target_id
        self.method = "GET"


class ListNegativeTargetingRequest(ListTargetingRequest):

    def __init__(self, target_ids: list = None, campaign_ids: list = None, ad_group_ids: list = None, states: list = None, start_index: int = 0, count: int = 100):
        super().__init__(target_ids=target_ids, campaign_ids=campaign_ids,
                         ad_group_ids=ad_group_ids, states=states, start_index=start_index, count=count)
        self.api = "/v2/sp/negativeTargets"


class ListNegativeTargetingExtendedRequest(ListTargetingRequest):

    def __init__(self, target_ids: list = None, campaign_ids: list = None, ad_group_ids: list = None, states: list = None, start_index: int = 0, count: int = 100):
        super().__init__(target_ids=target_ids, campaign_ids=campaign_ids,
                         ad_group_ids=ad_group_ids, states=states, start_index=start_index, count=count)
        self.api = "/v2/sp/targets/extended"


class CreateNegativeTargetingRequest(AbstractRequest):
    def __init__(self, negative_targetings: list = None):
        super.__init__()
        self.negative_targetings = negative_targetings and negative_targetings or []
        self.method = "POST"
        self.api = "/v2/sp/negativeTargets"

    def add_negative_targeting(self, negative_targeting:dict):
        self.negative_targetings.append(negative_targeting)

    def build_args(self):
        return self.negative_targetings


class ArchiveNegativeTargetingRequest(CreateNegativeTargetingRequest):
    def __init__(self, targetings: list = None):
        super.__init__(targetings)
        self.method = "DELETE"


class UpdateNegativeTargetingRequest(CreateNegativeTargetingRequest):
    def __init__(self, targetings: list = None):
        super.__init__(targetings)
        self.method = "PUT"
