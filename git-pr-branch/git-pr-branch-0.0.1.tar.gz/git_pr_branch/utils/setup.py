import re

import click

from git_pr_branch.config import conf


def setup_config():
    click.echo(
        "You have no configuration yet. Please answer the follwing question and "
        "I will create one for you."
    )
    click.echo(
        "Enter your Github personal token. If you don't have one yet, go to "
        "https://github.com/settings/tokens and create one."
    )
    github_token = click.prompt("Your Github personal token").strip()
    github_token_re = re.compile(r"[0-9a-f]{40}")
    while github_token_re.match(github_token) is None:
        github_token = click.prompt(
            "Hmm, this does not look like a Github token, please enter it again"
        ).strip()
    conf["github_token"] = github_token
    conf.write()
    click.echo(f"Your configuration is saved in {conf.path}")
