import click
import json
import config
import client


@click.group()
@click.option("--env", default="test")
@click.pass_context
def root(ctx, env):
    ctx.ensure_object(dict)
    cfg = config.Config(env)
    ctx.obj["client"] = client.Client(cfg)


@root.command()
@click.option("--phone", required=True)
@click.option("--password", required=True)
@click.option("--org", required=True, help="creditor organization's id")
@click.pass_context
def login(ctx, phone, password, org):
    try:
        c: client.Client = ctx.obj["client"]
        c.login(phone, password, org)
        click.echo("logged in")
    except Exception as e:
        click.echo(e)


if __name__ == "__main__":
    root()
    
