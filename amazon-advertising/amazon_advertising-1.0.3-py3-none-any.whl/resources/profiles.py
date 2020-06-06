from advertising import AbstractRequest, NoArgsRequest

__all__ = ["ListProfilesRequest", "GetProfileRequest", "UpdateProfileRequest"]


class ListProfilesRequest(NoArgsRequest):
    def __init__(self):
        super().__init__()
        self.api = "/v2/profiles"
        self.method = "GET"


class GetProfileRequest(NoArgsRequest):
    def __init__(self, profile_id: str):
        super().__init__()
        self.profile_id = profile_id
        self.api = "/v2/profiles/%s" % self.profile_id
        self.method = "GET"


class UpdateProfileRequest(AbstractRequest):
    def __init__(self, profiles: list = None):
        super().__init__()
        self.api = "/v2/profiles"
        self.method = "PUT"
        self.profiles = profiles and profiles or []

    def add_profile(self, profile: dict):
        self.profiles.append(profile)

    def build_args(self):
        return self.profiles
