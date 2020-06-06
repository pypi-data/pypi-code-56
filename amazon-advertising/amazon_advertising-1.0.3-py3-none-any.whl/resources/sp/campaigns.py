from advertising import AbstractRequest, NoArgsRequest


class GetCampaignRequest(NoArgsRequest):
    def __init__(self, campaign_id: str):
        super().__init__()
        self.campaign_id = campaign_id
        self.api = "/v2/sp/campaigns/%s" % self.campaign_id
        self.method = "GET"


class GetCampaignExtendedRequest(NoArgsRequest):
    def __init__(self, campaign_id: str):
        super().__init__()
        self.campaign_id = campaign_id
        self.api = "/v2/sp/campaigns/extended/%s" % self.campaign_id
        self.method = "GET"


class CreateCampaignsRequest(AbstractRequest):
    def __init__(self, portfolio_id: str, campaigns: list = None):
        super().__init__()
        self.portfolio_id = portfolio_id
        self.campaigns = campaigns and campaigns or []
        self.api = "/v2/sp/campaigns"
        self.method = "POST"

    def add_campaign(self, campaign: dict):
        self.campaigns.append(campaign)

    def build_args(self):
        return {"portfolioId": self.portfolio_id,  "campaigns": self.campaigns}


class UpdateCampaignsRequest(AbstractRequest):
    def __init__(self, campaigns: list = None):
        super().__init__()
        self.campaigns = campaigns
        self.method = "PUT"

    def add_campaign(self, campaign: dict):
        self.campaigns.append(campaign)

    def build_args(self):
        return self.campaigns


class ArchiveCampaignRequest(NoArgsRequest):
    def __init__(self, campaign_id: str):
        super().__init__()
        self.campaign_id = campaign_id
        self.api = "/v2/sp/campaigns/%s" % self.campaign_id
        self.method = "DELETE"


class ListCampaignsRequest(AbstractRequest):
    def __init__(self,
                 name: str = None,
                 portfolio_id: str = None,
                 campaign_ids: list = None,
                 states: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):
        super().__init__()
        self.name = name
        self.portfolio_id = portfolio_id
        self.campaign_ids = campaign_ids and campaign_ids or []
        self.states = states and states or []
        self.start_index = start_index
        self.count = count
        self.api = "/v2/sp/campaigns"
        self.method = "GET"

    def build_args(self):

        return {
            "startIndex": self.start_index,
            "count": self.count,
            "name": self.name,
            "portfolioIdFilter": self.portfolio_id,
            "stateFilter": ",".join(self.states),
            "campaignIdFilter":  ",".join(self.campaign_ids)
        }


class ListCampaignsExtendedRequest(ListCampaignsRequest):
    def __init__(self,
                 name: str = None,
                 portfolio_id: str = None,
                 campaign_ids: list = None,
                 states: list = None,
                 start_index: int = 0,
                 count: int = 100
                 ):
        super().__init__()
        self.name = name
        self.portfolio_id = portfolio_id
        self.campaign_ids = campaign_ids and campaign_ids or []
        self.states = states and states or []
        self.start_index = start_index
        self.count = count
        self.api = "/v2/sp/campaigns/extended"
        self.method = "GET"
