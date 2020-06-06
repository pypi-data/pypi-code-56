import os
import click
import requests
import docker

DEBUG = False
CATACOMB_URL = 'http://localhost:8000' if DEBUG else 'https://catacomb.ai'

@click.command()
def cli():
    name = click.prompt("🤖 Image name", type=str)
    docker_username = click.prompt("🤖 Docker account username", type=str)
    repository = docker_username + '/' + name

    click.echo("""\n🤖 Got it! Building your Docker image (this may take a while)...""")

    client = docker.from_env()
    image = client.images.build(path='./', tag={repository})
    print(image)

    for line in client.images.push(repository, stream=True, decode=True):
        click.echo(line)

    click.echo("""\n🤖 We've pushed your system's image to: https://hub.docker.com/r/{}/.""".format(repository))

    try:
        r = requests.post('{}/api/upload/'.format(CATACOMB_URL), json={'image': repository, 'name': name})
        image = r.json()['image']
        click.echo('Almost done! Finalize and deploy your system at: {}/upload/image/{}/'.format(CATACOMB_URL, image))
    except Exception as error:
        print(error)
        click.echo("Something went wrong! Ensure your system includes all the necessary components and try again.")

    # click.echo("""\n🤖 Your system is live at: https://catacomb.ai/username/{}/""".format(name))