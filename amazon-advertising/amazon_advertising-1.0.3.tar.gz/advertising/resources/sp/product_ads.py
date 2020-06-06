from advertising import AbstractRequest, NoArgsRequest


class GetProductAdRequest(NoArgsRequest):
    def __init__(self, ad_id: str):
        super().__init__()
        self.ad_id = ad_id
        self.api = "/v2/sp/productAds/%s" % self.ad_id
        self.method = "GET"


class GetProductAdExtendedRequest(NoArgsRequest):
    def __init__(self, ad_id: str):
        super().__init__()
        self.ad_id = ad_id
        self.api = "/v2/sp/productAds/extended/%s" % self.ad_id
        self.method = "GET"


class CreateProductAdsRequest(AbstractRequest):
    def __init__(self, product_ads: list = None):
        super().__init__()
        self.product_ads = product_ads and product_ads or []
        self.apt = "/v2/sp/productAds"
        self.method = "POST"

    def add_product_ad(self, product_ad:dict):
        self.product_ads.append(product_ad)

    def build_args(self):
        return self.product_ads


class UpdateProductAdsRequest(CreateProductAdsRequest):
    def __init__(self, product_ads: list = None):
        super().__init__(product_ads)
        self.method = "PUT"


class ArchiveProductAdRequest(NoArgsRequest):
    def __init__(self, product_ad: str):
        super().__init__()
        self.product_ad = product_ad
        self.api = "/v2/sp/productAds/%s" % self.product_ad
        self.method = "DELETE"


class ListProductAdsRequest(AbstractRequest):
    def __init__(self, ad_ids: list = None, campaign_ids: list = None, ad_group_ids: list = None, states: list = None, start_index: int = 0, count: int = 100):
        super().__init__()
        self.ad_ids = ad_ids and ad_ids or []
        self.campaign_ids = campaign_ids and campaign_ids or []
        self.ad_group_ids = ad_group_ids and ad_group_ids or []
        self.states = states and states or []
        self.start_index = start_index
        self.count = count
        self.api = "/v2/sp/productAds/"
        self.method = "GET"

    def build_args(self):

        return {
            "startIndex": self.start_index,
            "count": self.count,
            "stateFilter": ",".join(self.states),
            "campaignIdFilter":  ",".join(self.campaign_ids),
            "adGroupIdFilter":  ",".join(self.ad_group_ids),
            "adIdFilter": ",".join(self.ad_ids)
        }


class ListProductAdsExtendedRequest(ListProductAdsRequest):
    def __init__(self, ad_ids: list = None, campaign_ids: list = None, ad_group_ids: list = None, states: list = None, start_index: int = 0, count: int = 100):
        super().__init__(ad_ids=ad_ids, campaign_ids=campaign_ids,
                         ad_group_ids=ad_group_ids, states=states, start_index=start_index, count=count)
        self.api = "/v2/sp/productAds/extended"
