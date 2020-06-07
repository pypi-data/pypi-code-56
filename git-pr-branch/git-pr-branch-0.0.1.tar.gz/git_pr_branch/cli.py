import os

import click

from .config import conf
from .repo import GitRepo
from .utils.cli import AliasedGroup
from .utils.relationship import get_remote_for_pr, create_pr_branch
from .utils.setup import setup_config


@click.command(cls=AliasedGroup)
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(exists=True),
    help="Path to the configuration file",
)
@click.pass_context
def cli(ctx, config_path):
    """Manage branches and pull-requests"""
    ctx.ensure_object(dict)
    if not os.path.exists(conf.path):
        setup_config()

    conf.load(config_path)
    if not conf["github_token"]:
        message = (
            "you must set the github_token in the config file. "
            f"The config file will be loaded from {conf.path}"
        )
        message.extend([f"- {p}" for p in conf.load_paths])
        raise click.ClickException("\n".join(message))
    ctx.obj["repo"] = GitRepo()


@cli.command()
@click.pass_context
def show(ctx):
    """Show branches and pull requests"""
    repo = ctx.obj["repo"]
    branches = repo.get_branches()
    max_length = max([len(b.name) for b in branches])
    origin_repo = repo.get_branch("master").get_remote().get_server_repo()
    for branch in branches:
        click.echo(branch.name.ljust(max_length), nl=False)
        pulls = origin_repo.get_pulls(branch)
        for pr in pulls:
            info = [
                f"#{pr.number}".ljust(4),
                f"[{pr.state}]".ljust(8),
                f"{pr.html_url}",
            ]
            click.echo("\t" + "    ".join(info), nl=False)
        click.echo()


@cli.command()
@click.option(
    "--remotes/--no-remotes",
    "prune_remotes",
    default=True,
    show_default=True,
    help="Also prune remote references",
)
@click.pass_context
def prune(ctx, prune_remotes):
    """Remove branches whose pull requests are closed"""
    repo = ctx.obj["repo"]
    to_prune = []
    origin_repo = repo.get_branch("master").get_remote().get_server_repo()
    click.echo("Branches to prune:")
    for branch in repo.get_branches():
        pulls = origin_repo.get_pulls(branch)
        if not pulls:
            continue
        if all([pr.state == "closed" for pr in pulls]):
            click.echo(branch.name)
            to_prune.append(branch)
    if to_prune:
        answer = click.confirm("Should they be deleted locally?")
        if answer:
            current_branch = repo.get_current_branch()
            if current_branch in to_prune:
                repo.get_branch("master").checkout()
            for branch in to_prune:
                branch.delete(force=True)
        else:
            click.echo("OK, aborting here.")
    else:
        click.echo("No branch to prune.")
    if prune_remotes:
        click.secho("Cleaning up remote references", fg="bright_blue")
        for remote in repo.get_remotes():
            remote.prune()


@cli.command(alias="co")
@click.argument("pr-number", type=int)
@click.pass_context
def checkout(ctx, pr_number):
    """Check out a pull request in a local branch"""
    repo = ctx.obj["repo"]
    pr_branches = [
        b for b in repo.get_branches() if b.name.startswith(f"PR/{pr_number}/")
    ]
    master_branch = repo.get_branch("master")
    origin_remote = master_branch.get_remote()
    origin_repo = origin_remote.get_server_repo()
    pr = origin_repo.get_pull(pr_number)

    if pr.state == "closed":
        answer = click.confirm(
            "This PR is closed, are you sure you want to check it out?"
        )
        if not answer:
            click.echo("Aborting.")
            return

    # Move to master
    master_branch.checkout(quiet=True)
    # Get or create the remote for this PR
    remote = get_remote_for_pr(repo, pr)
    remote.fetch()
    branch_id = len(pr_branches) + 1
    if branch_id == 1:
        # Initial checkout: also check out previous reviews
        for review in pr.get_reviews():
            if review.username == pr.username:
                # Review requests show up as review comments in the API
                continue
            timestamp = review.datetime.strftime("%x %X")
            click.secho(
                f"Checking out review by {review.username} on {timestamp} with state "
                f"{review.state} to sub-branch {branch_id}",
                fg="bright_cyan",
            )
            create_pr_branch(pr, branch_id, remote, review.commit_id)
            branch_id += 1

    click.secho(
        f"Checking out PR #{pr.number} to sub-branch {branch_id}", fg="bright_cyan"
    )
    branch = create_pr_branch(pr, branch_id, remote, pr.head_commit)
    branch.checkout()
