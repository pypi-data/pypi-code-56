import click
from .manage_secrets import get_value_from_parameter_store as get_ssm


@click.group()
def entrypoint():
    pass


@entrypoint.command()
@click.option('--name', required=True,
              help='Name of parameter to get value from SSM')
def get(name):
    """get secrets"""
    print(get_ssm(name))


if __name__ == "__main__":
    entrypoint()
