import click

NOTIFY_CREATED_DEPLOY_MSG_FMT = '''
  Created deploy:
    current_version.tag={current_tag}
    previous_version.tag={previous_tag}
'''


def notify_created_deploy(deploy):
    msg = NOTIFY_CREATED_DEPLOY_MSG_FMT.format(
        **deploy
    )

    click.echo(msg)
