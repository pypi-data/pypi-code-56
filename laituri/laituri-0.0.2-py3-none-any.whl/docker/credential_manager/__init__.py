from typing import Callable, Dict, Optional

from .credential_managers import credential_managers
from .dummy import dummy_credential_manager


def _noop_log_status(message: str):
    pass  # pragma: nocover


def get_credential_manager(
    *,
    image: str,
    registry_credentials: Optional[Dict] = None,
    log_status: Optional[Callable] = _noop_log_status
):
    """
    Get a credential context manager object based on the registry credentials dictionary passed in.

    If registry credentials are missing or incomplete, will still trigger the wrapped action.
    If registry credentials are invalid, raises DockerLoginFailed.

    :param image: full Docker image name, including the registry domain and tag if applicable
    :param registry_credentials: optional {type, version, username, password} dict for registry login
    :param log_status: optional function to use for user-facing status logging
    :raises DockerLoginFailed
    :return: ContextManager
    """
    manager_kwargs = dict(
        image=image,
        registry_credentials=registry_credentials,
        log_status=log_status,
    )
    if not isinstance(registry_credentials, dict):  # no credentials to manage
        return dummy_credential_manager(**manager_kwargs)

    type = registry_credentials.get('type')
    version = registry_credentials.get('version')
    manager = credential_managers.get((type, version))
    if manager:
        return manager(**manager_kwargs)

    log_status('Unable to parse %s version %s registry credentials; upcoming action may fail.' % (type, version))
    return dummy_credential_manager(**manager_kwargs)
