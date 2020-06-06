from advertising import AbstractRequest, NoArgsRequest


class GetAdGroupRequest(NoArgsRequest):
    def __init__(self, ad_group_id: str):
        super().__init__()
        self.ad_group_id = ad_group_id
        self.api = "/v2/sp/adGroups/%s" % self.ad_group_id
        self.method = "GET"


class GetAdGroupExtendedRequest(NoArgsRequest):
    def __init__(self, ad_group_id: str):
        super().__init__()
        self.ad_group_id = ad_group_id
        self.api = "/v2/sp/adGroups/extended/%s" % self.ad_group_id
        self.method = "GET"


class CreateAdGroupsRequest(AbstractRequest):
    def __init__(self, ad_groups: list = None):
        super.__init__()
        self.ad_groups = ad_groups and ad_groups or []
        self.api = "/v2/sp/adGroups"
        self.method = "POST"

    def add_ad_group(self, ad_group: dict):
        self.ad_groups.append(ad_group)

    def build_args(self):
        return self.ad_groups


class UpdateAdGroupsRequest(CreateAdGroupsRequest):
    def __init__(self, ad_groups: list = None):
        super.__init__(ad_groups=ad_groups)
        self.method = "PUT"


class ArchiveAdGroupRequest(AbstractRequest):
    def __init__(self, ad_group_id: str):
        super().__init__()
        self.ad_group_id = ad_group_id
        self.api = "/v2/sp/adGroups/%s" % self.ad_group_id
        self.method = "DELETE"


class ListAdGroupsRequest(AbstractRequest):
    def __init__(self,
                 name: str = None,
                 campaign_type: str = None,
                 campaign_ids: list = None,
                 ad_group_ids: list = None,
                 states: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):
        super().__init__()
        self.name = name
        self.campaign_type = campaign_type
        self.campaign_ids = campaign_ids and campaign_ids or []
        self.ad_group_ids = ad_group_ids and ad_group_ids or []
        self.states = states and states or []
        self.start_index = start_index
        self.count = count
        self.api = "/v2/sp/adGroups"
        self.method = "GET"

    def build_args(self):

        return {
            "startIndex": self.start_index,
            "count": self.count,
            "name": self.name,
            "campaignType": self.campaign_type,
            "stateFilter": ",".join(self.states),
            "campaignIdFilter":  ",".join(self.campaign_ids),
            "adGroupIdFilter":  ",".join(self.ad_group_ids),
        }


class ListAdGroupsExtendedRequest(ListAdGroupsRequest):
    def __init__(self,
                 name: str = None,
                 campaign_type: str = None,
                 campaign_ids: list = None,
                 ad_group_ids: list = None,
                 states: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):
        super().__init__(name=name, campaign_type=campaign_type, campaign_ids=campaign_ids,
                         ad_group_ids=ad_group_ids, states=states, start_index=start_index, count=count)
        self.api = "/v2/sp/adGroups/extended"
