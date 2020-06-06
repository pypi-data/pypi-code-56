from advertising import AbstractRequest

__all__ = ["GetKeywordRecommendations"]


class GetKeywordRecommendations(AbstractRequest):

    def __init__(self, asins: list = None, url: str = None, max_num_suggestion: int = 100):
        super().__init__()
        self.asins = asins
        self.url = url
        self.max_num_suggestion = max_num_suggestion
        self.api = "/sb/recommendations/keyword"
        self.method = "POST"

    def build_args(self):
        if self.asins is None and self.url is None:
            raise ValueError("Specifies the url or asins")

        args = {
            "maxNumSuggestions": self.max_num_suggestion,
            "asins": self.asins,
            "url": self.url
        }
        return args
