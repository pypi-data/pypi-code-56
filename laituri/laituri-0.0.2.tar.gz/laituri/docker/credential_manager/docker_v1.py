import logging
import subprocess
from contextlib import contextmanager
from typing import Callable, Dict

from laituri import settings

from .errors import DockerLoginFailed

log = logging.getLogger(__name__)


def docker_login(domain: str, username: str, password: str) -> bool:
    """Use Docker command-line client to login to the specified image registry."""
    args = [
        '/usr/bin/env',
        settings.DOCKER_COMMAND,
        'login',
        '--username', username,
        '--password-stdin',
        domain,
    ]
    log.info('Running `%s`' % ' '.join(args))
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        cmd_input = (password + '\n').encode('utf-8')
        stdout, _ = proc.communicate(input=cmd_input, timeout=settings.DOCKER_TIMEOUT)
    except subprocess.TimeoutExpired as te:
        raise DockerLoginFailed('timed out') from te
    if proc.returncode != 0:
        raise DockerLoginFailed(stdout.decode('utf-8', errors='ignore'))
    return True


def docker_logout(domain: str) -> None:
    """Use Docker command-line client to logout from the specified image registry."""
    # Hack: when logging out of "docker.io" they actually mean "https://index.docker.io/v1/"...
    if domain == 'docker.io':
        domain = 'https://index.docker.io/v1/'

    try:
        log.info('Running `docker logout %s`' % domain)
        subprocess.check_call([
            '/usr/bin/env',
            settings.DOCKER_COMMAND,
            'logout',
            domain,
        ], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, timeout=settings.DOCKER_TIMEOUT)
    except subprocess.CalledProcessError as cpe:
        message = cpe.stdout.decode('utf-8', errors='ignore')
        log.warning('Failed `docker logout %s`: %s' % (domain, message))


@contextmanager
def docker_v1_credential_manager(
    *,
    image: str,
    registry_credentials: Dict,
    log_status: Callable
):
    """Credential context manager that tries to log you in before the context and logs out out on exit."""
    domain = image.split('/')[0]
    try:
        docker_login(
            domain=domain,
            username=str(registry_credentials['username']),
            password=str(registry_credentials['password']),
        )
    except DockerLoginFailed as dlf:
        raise DockerLoginFailed('Failed Docker login to %s: %s' % (domain, str(dlf))) from dlf

    yield  # do your thing

    docker_logout(domain)
