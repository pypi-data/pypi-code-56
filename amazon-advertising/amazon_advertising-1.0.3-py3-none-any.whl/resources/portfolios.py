from advertising import AbstractRequest, NoArgsRequest

__all__ = []


class ListPortfoliosRequest(AbstractRequest):
    def __init__(self, portfolio_id: list = None, portfolio_name: str = None, portfolio_state: str = None):
        super().__init__()
        self.api = "/v2/portfolios"
        self.method = "GET"
        self.portfolio_id = portfolio_id
        self.portfolio_name = portfolio_name
        self.portfolio_state = portfolio_state

    def build_args(self):
        return {
            "portfolioStateFilter": self.portfolio_state,
            "portfolioNameFilter": self.portfolio_name,
            "portfolioIdFilter": self.portfolio_id,
        }


class ListPortfoliosExtendedRequest(ListPortfoliosRequest):
    def __init__(self, portfolio_id: list = None, portfolio_name: str = None, portfolio_state: str = None):
        super().__init__(portfolio_id, portfolio_name, portfolio_state)
        self.api = "/v2/portfolios/extended"


class GetPortfolioRequest(NoArgsRequest):
    def __init__(self, protfolio_id: str):
        super.__init__()
        self.protfolio_id = protfolio_id
        self.api = "/v2/portfolios/%s" % self.protfolio_id
        self.method = "GET"


class GetPortfolioExtendedRequest(NoArgsRequest):
    def __init__(self, protfolio_id: str):
        super.__init__()
        self.protfolio_id = protfolio_id
        self.api = "/v2/portfolios/extended/%s" % self.protfolio_id
        self.method = "GET"


class CreateProtfoliosRequest(AbstractRequest):
    def __init__(self, portfolios: list = None):
        super.__init__()
        self.portfolios = portfolios
        self.api = "/v2/portfolios"
        self.method = "POST"

    def add_protfolio(self, protfolio: dict):
        self.portfolios.append(protfolio)

    def build_args(self):
        return self.portfolios


class UpdateProtfoliosRequest(CreateProtfoliosRequest):
    def __init__(self, portfolios: list = None):
        super.__init__(portfolios)
        self.method = "PUT"
