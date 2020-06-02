import datetime
from typing import Mapping, Any, List

from git import Repo, Commit


def fetch_git_history(path: str, email: str, config: Mapping[str, Any]) -> List[Commit]:
    repo = Repo(path)
    since_date = datetime.date.today() - datetime.timedelta(days=config['history_depth_years'] * 365)
    commits = list(repo.iter_commits(since=since_date, no_merges=True))
    return [c for c in commits if c.author.email == email]
