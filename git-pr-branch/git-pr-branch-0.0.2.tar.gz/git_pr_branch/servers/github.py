import datetime
from urllib.parse import urlparse

import attr
import requests
from dateutil.parser import isoparse

from git_pr_branch.config import conf


@attr.s(auto_attribs=True)
class PR:
    number: int
    url: str
    state: str
    html_url: str
    head_fullname: str
    head_username: str
    head_branch: str
    head_commit: str
    head_ssh: str
    username: str

    @classmethod
    def from_github(cls, data):
        return cls(
            number=data["number"],
            url=data["url"],
            state=data["state"],
            html_url=data["html_url"],
            head_fullname=data["head"]["repo"]["full_name"],
            head_username=data["head"]["repo"]["owner"]["login"],
            head_branch=data["head"]["ref"],
            head_commit=data["head"]["sha"],
            head_ssh=data["head"]["repo"]["ssh_url"],
            username=data["user"]["login"],
        )

    def get_reviews(self):
        response = requests.get(
            f"{self.url}/reviews", auth=("git-pr", conf["github_token"]),
        )
        if not response.ok:
            raise GithubAPIError(response.text)
        reviews = response.json()
        return [Review.from_github(review) for review in reviews]


@attr.s(auto_attribs=True)
class Review:
    id: int
    commit_id: str
    html_url: str
    username: str
    state: str
    datetime: datetime.datetime
    body: str

    @classmethod
    def from_github(cls, data):
        return cls(
            id=data["id"],
            commit_id=data["commit_id"],
            html_url=data["html_url"],
            username=data["user"]["login"],
            state=data["state"],
            datetime=isoparse(data["submitted_at"]),
            body=data["body"],
        )


@attr.s(auto_attribs=True)
class GithubAPIError(Exception):
    message: str


@attr.s(auto_attribs=True)
class GithubRepo:

    username: str
    reponame: str
    _cache_pulls: dict = attr.ib(init=False, factory=dict)
    _clone_url_prefixes = (
        "git@github.com:",
        "https://github.com/",
    )

    @classmethod
    def owns_url(cls, url):
        for prefix in cls._clone_url_prefixes:
            if url.startswith(prefix):
                return True
        return False

    @classmethod
    def from_url(cls, url):
        if url.startswith("https://"):
            path = urlparse(url).path[1:]
        else:
            path = url.split(":", 1)[1]
        username, repo = path.split("/", 1)
        if repo.endswith(".git"):
            repo = repo[: -len(".git")]
        return cls(username=username, reponame=repo)

    @property
    def fullname(self):
        return f"{self.username}/{self.reponame}"

    def get_pulls(self, branch):
        remote = branch.get_remote()
        remote_ref = branch.get_merge_ref()
        if remote is None or remote_ref is None:
            return []
        fork_repo = remote.get_server_repo()
        head = f"{fork_repo.username}:{remote_ref}"
        if head not in self._cache_pulls:
            url = (
                f"https://api.github.com/repos/{self.username}/{self.reponame}/pulls?"
                f"state=all&head={head}"
            )
            response = requests.get(url, auth=("git-pr", conf["github_token"]),)
            if not response.ok:
                raise GithubAPIError(response.text)
            pulls = response.json()
            self._cache_pulls[head] = [PR.from_github(pr) for pr in pulls]
        return self._cache_pulls[head]

    def get_pull(self, number):
        response = requests.get(
            f"https://api.github.com/repos/{self.username}/{self.reponame}/pulls/{number}",
            auth=("git-pr", conf["github_token"]),
        )
        if not response.ok:
            raise GithubAPIError(response.text)
        return PR.from_github(response.json())
