from __future__ import unicode_literals, absolute_import

import os

import click
from fedora_messaging.config import conf

import robosignatory.work
from robosignatory.tag import TagSigner
from robosignatory.coreos import (
    CoreOSSigner, ArtifactSignerWrapper, OSTreeSignerWrapper, SigningFailed
)
from robosignatory import utils


@click.group()
@click.option(
    "-c", "--config",
    default="/etc/fedora-messaging/robosignatory.toml",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the configuration file"
)
def cli(config):
    if not os.path.isfile(config):
        raise click.exceptions.BadParameter("{} is not a file".format(config))
    conf.load_config(config_path=config)
    conf.setup_logging()


@cli.command("sign-tag")
@click.option("--tag", is_flag=True)
@click.argument("koji_instance")
@click.argument("build_nvr")
@click.argument("curtag")
def tag(tag, koji_instance, build_nvr, curtag):
    skiptag = not tag
    signer = TagSigner(conf["consumer_config"])
    signer.dowork(build_nvr, None, curtag, koji_instance, skiptag)


@cli.command("sign-atomic")
@click.option("--ref-update", is_flag=True)
@click.argument("ref")
@click.argument("commitid")
def atomic(ref_update, ref, commitid):
    if ref not in conf["consumer_config"]["ostree_refs"]:
        click.fail('Ref %s not found' % ref)
    signing_config = conf["consumer_config"]["signing"]
    signer = utils.get_signing_helper(**signing_config)
    val = conf["consumer_config"]["ostree_refs"][ref]
    robosignatory.work.process_atomic(
        signer, ref, commitid, doref=ref_update, **val)


@cli.command("sign-coreos-artifact")
@click.argument("file_url")
@click.argument("checksum")
def coreos_artifact(file_url, checksum):
    consumer = CoreOSSigner(conf["consumer_config"])
    key = consumer.get_key(None)
    signing_wrapper = ArtifactSignerWrapper(consumer.signer, key, consumer.bucket)
    try:
        signing_wrapper.sign(file_url, checksum)
    except SigningFailed as e:
        click.fail(str(e))


@cli.command("sign-coreos-ostree")
@click.argument("file_url")
@click.argument("checksum")
def coreos_ostree(file_url, checksum):
    consumer = CoreOSSigner(conf["consumer_config"])
    key = consumer.get_key(None)
    signing_wrapper = OSTreeSignerWrapper(consumer.signer, key, consumer.bucket)
    try:
        signing_wrapper.sign(file_url, checksum)
    except SigningFailed as e:
        click.fail(str(e))
