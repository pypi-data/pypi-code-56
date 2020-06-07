from github import Github

from colorama import Fore, Style

from .utils import CredsManager, salir, info, error


class GithubClient:

    def __init__(self, cfg):
        self.creds = CredsManager()
        self.TOKEN = self.creds.get_token("github")
        self.SRV = cfg.server
        self.USR = cfg.username
        self.REPO = cfg.repo
        self.link = cfg.link

        self.g = Github(self.TOKEN)
        try:
            self.r = self.g.get_repo(f"{self.USR}/{self.REPO}")
        except Exception as e:
            print(e.args)
            salir("Github client can't connect")

    # ─── COMMANDS ───────────────────────────────────────────────────────────────────

    def list_issues(self):
        issues_list = self.open_issues
        for i in issues_list:
            print(f"  {Style.BRIGHT}{i.number} {Style.DIM}{i.title.title()}")
        if len(issues_list) == 0:
            print(f"    {Style.DIM}There no open issues assigned at current Milestone ")

    def close_issue(self, id):
        issue = self.r.get_issue(number=int(id))
        issue.edit(state='closed')

    def show_issue(self, id):
        issue = self.r.get_issue(number=int(id))
        print(issue.url)
        print(issue.title)
        print(issue.body)

    def new_issue(self, labels):
        title = input("Input title: ")
        body = input("Input contents: ")
        self.r.create_issue(title=title, body=body, labels=labels)

    # ─── PROPERTIES ─────────────────────────────────────────────────────────────────

    @property
    def open_issues(self):
        lista = []
        for i in self.r.get_issues():
            if i.milestone is not None:
                if i.milestone.state == "open":
                    lista.append(i)
        return lista

# ────────────────────────────────────────────────────────────────────────────────
