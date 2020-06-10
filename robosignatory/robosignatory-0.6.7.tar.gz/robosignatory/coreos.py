from __future__ import unicode_literals, absolute_import

import os
import stat
import logging
import shutil
import tempfile

import boto3
import robosignatory.utils as utils
from botocore.exceptions import ClientError
from six.moves.urllib.parse import urlparse
from fedora_messaging.api import Message, publish


log = logging.getLogger(__name__)


class CoreOSSigner(object):

    def __init__(self, config):
        self.config = config

        aws_config = self.config['coreos']['aws']
        s3 = boto3.resource(
            's3',
            region_name=aws_config['region'],
            aws_access_key_id=aws_config['access_key'],
            aws_secret_access_key=aws_config['access_secret'],
        )
        bucket_name = self.config['coreos']['bucket']
        self.bucket = s3.Bucket(bucket_name)

        signing_config = self.config['signing']
        self.signer = utils.get_signing_helper(**signing_config)

        log.info('CoreOSSigner ready for service')

    def get_key(self, msg):
        # Evaluation of the key is here and not in __init__ because we may want
        # a stream or version-dependant key in the future.

        # If there is a key hardcoded in the config then use that.
        # This is useful in the staging environment where we only have
        # one key.
        config_key = self.config["coreos"].get("key")
        if config_key:
            return config_key
        # Detect what key to use by using the first digits of the
        # build_id (in the form of `"build_id": "32.20200527.20.0"`).
        major = int(msg.body["build_id"].split('.')[0])
        return 'fedora-' + str(major)

    def consume(self, msg):
        # Message structure:
        # https://github.com/coreos/fedora-coreos-tracker/issues/198#issuecomment-513944390
        log.info(
            'CoreOS wants to sign '
            '%(build_id)s for %(basearch)s' % msg.body
        )
        key = self.get_key(msg)

        response = Message(
            topic="{}.finished".format(msg.topic),
            # respond with the same body, but clone so we keep the original one
            body=dict(msg.body)
        )

        try:
            if msg.topic.endswith('.coreos.build.request.artifacts-sign'):
                wrapper = ArtifactSignerWrapper(self.signer, key, self.bucket)
                for artifact in msg.body["artifacts"]:
                    wrapper.sign(artifact["file"], artifact["checksum"])

            elif msg.topic.endswith('.coreos.build.request.ostree-sign'):
                wrapper = OSTreeSignerWrapper(self.signer, key, self.bucket)
                wrapper.sign(msg.body["commit_object"], msg.body["checksum"])
        except SigningFailed as e:
            log.error(e)
            response.body["status"] = "FAILURE"
            response.body["failure-message"] = str(e)
            publish(response)
        else:
            response.body["status"] = "SUCCESS"
            publish(response)


class SigningFailed(Exception):
    pass


class SignerWrapper(object):
    """
    This class handles the common operations that come with signing a file in S3.
    """

    def __init__(self, signer, key, bucket):
        self.signer = signer
        self.key = key
        self.bucket = bucket

    def _get_sig_filepath(self, filepath, checksum):
        raise NotImplementedError

    def _get_cmdline(self, filepath):
        raise NotImplementedError

    def sign(self, url, checksum):
        if ':' not in checksum:
            raise SigningFailed("Missing algo prefix in {}".format(checksum))
        algo, checksum = checksum.split(':', 1)
        if algo != "sha256":
            # for now, we only handle sha256
            raise SigningFailed("Unknown checksum algo {}".format(algo))
        tmpdir = tempfile.mkdtemp(prefix="/tmp/robosignatory-")
        try:
            self._sign_object(url, checksum, tmpdir)
        finally:
            shutil.rmtree(tmpdir)

    def _sign_object(self, url, checksum, tmpdir):
        filepath = urlparse(url).path.lstrip("/")
        local_filepath = os.path.join(tmpdir, os.path.basename(filepath))

        log.info("Downloading %s", filepath)
        try:
            self.bucket.download_file(filepath, local_filepath)
        except ClientError as e:
            raise SigningFailed("Could not download {}: {}".format(filepath, e))

        log.info("Checking hash for %s", filepath)
        if utils.get_hash(local_filepath) != checksum:
            raise SigningFailed("Incorrect SHA256 for {}, not signing".format(filepath))

        log.info("Signing %s", filepath)
        sig_filepath = self._get_sig_filepath(local_filepath)
        cmdline = self._get_cmdline(local_filepath, checksum)
        log.info('Signing command line: %s', cmdline)
        ret, stdout, stderr = utils.run_command(cmdline)
        if ret != 0:
            raise SigningFailed(
                'Error signing! Signing output: {}, stdout: {}, stderr: {}'.format(
                    ret, stdout, stderr)
            )
        if not os.path.exists(sig_filepath):
            raise SigningFailed(
                "Signer did not produce any signature file for {}".format(filepath)
            )
        log.debug('Fixing signature file permissions')
        # Sigul writes it as 0600, which makes a lot of sense as a general file
        # mode for it, but this is just a signature file that we want published
        os.chmod(sig_filepath,
                 (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH))

        log.info("Uploading signature for %s", filepath)
        uploaded_sig_filepath = self._get_sig_filepath(filepath)
        self.bucket.upload_file(sig_filepath, uploaded_sig_filepath)
        # Check the uploaded file
        uploaded = list(self.bucket.objects.filter(Prefix=uploaded_sig_filepath))
        if len(uploaded) != 1:
            log.warning("The signature for %s was not uploaded properly", filepath)
        elif uploaded[0].size != os.stat(sig_filepath).st_size:
            log.warning(
                "The uploaded signature for %s does not have the right size",
                filepath
            )

        os.remove(local_filepath)
        os.remove(sig_filepath)


class ArtifactSignerWrapper(SignerWrapper):

    def _get_sig_filepath(self, filepath):
        return filepath + ".sig"

    def _get_cmdline(self, filepath, checksum):
        return self.signer.build_coreos_cmdline(
            self.key, filepath, self._get_sig_filepath(filepath))


class OSTreeSignerWrapper(SignerWrapper):

    SIG_NAME = "ostree-commitmeta-object"

    def _get_sig_filepath(self, filepath):
        return "/".join([os.path.dirname(filepath), self.SIG_NAME])

    def _get_cmdline(self, filepath, checksum):
        return self.signer.build_atomic_cmdline(
            self.key, checksum, filepath, self._get_sig_filepath(filepath))
