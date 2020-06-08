import getpass
from pathlib import Path
from typing import Any, Dict, Optional

import hvac
import requests
from dbt.exceptions import RuntimeException
from dbt.logger import GLOBAL_LOGGER as logger


def from_url(url: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
    """Load data from url

    Args:
        url (str): [description]
        params (Optional[Dict[str, Any]], optional): [description]. Defaults to None.

    Returns:
        requests.Response: [description]
    """
    result = requests.get(url=url, params=params)
    logger.info(f"[JINJA2] Request [{result.url}]: {result.status_code}")
    return result


def from_file(filepath: str) -> str:
    """Load data from file

    Args:
        filepath (str): filepath

    Returns:
        str: file content
    """
    path_ = Path(filepath)
    logger.info(f"[JINJA2] Reading from file {str(path_)}")
    result = path_.read_text()
    return result


def from_vault_token(url: str, token: str, verify=False) -> hvac.Client:
    """Create client of Hashicorp Vault. Token authorization.

    Args:
        url (str): vault url
        token (str): authorization token
        verify (bool): wheter verify TLS

    Returns:
        hvac.Client: vault client.
    """
    client = hvac.Client(url=url, token=token, verify=verify)
    logger.info(f"[JINJA2] Vault {url} authenticated {client.is_authenticated()}")
    return client


def from_vault_ldap(
    url: str, username: str, password: str, verify=False,
) -> hvac.Client:
    """Create client of Hashicorp Vault. LDAP authorization.

    Args:
        url (str): vault url
        username (str): ldap username
        password (str): ldap password
        verify (bool): wheter verify TLS

    Returns:
        hvac.Client: vault client.
    """
    client = hvac.Client(url=url, verify=verify)
    client.auth.ldap.login(username=username, password=password)
    logger.info(f"[JINJA2] Vault {url} authenticated {client.is_authenticated()}")
    return client


def whoami() -> str:
    """Get current username.

    Returns:
        str: username
    """
    return getpass.getuser()


def exception(text: str):
    """Raise exception.

    Args:
        text (str): error text

    Raises:
        RuntimeException: error
    """
    raise RuntimeException(text)
