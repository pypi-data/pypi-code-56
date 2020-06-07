import sys

from .utils import SettingsFile, get_version, print_header, salir, info, error
from .github import GithubClient


def get_client():
    # check settings file and create if not exist
    config = SettingsFile()
    if not config.exist:
        config.create()
    # devuelve cliente del server que toca
    if config.server == "github.com":
        return GithubClient(config)
    else:
        salir("Server not implemented")


def run_handler(args):
    print_header()

    if args['--version']:
        info(f"Current version: {get_version()}")
        sys.exit()

    client = get_client()

    if args['--list']:
        info("Listing all open issues from current Milestone...\n")
        client.list_issues()

    elif args['--new']:
        info("Creating new generic isse...")
        client.new_issue([])

    elif args['--bug']:
        info("Creating new bug isse...")
        client.new_issue(['bug'])

    elif args['--show'] and args['<id>'] is not None:
        client.show_issue(args['<id>'])

    elif args['--close'] and args['<id>'] is not None:
        info("Closing issue...")
        client.close_issue(args['<id>'])

    print("")
