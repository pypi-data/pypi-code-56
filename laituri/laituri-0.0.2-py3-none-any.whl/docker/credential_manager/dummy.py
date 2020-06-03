from contextlib import contextmanager
from typing import Callable, Dict, Optional


@contextmanager
def dummy_credential_manager(
    *,
    image: str,
    registry_credentials: Optional[Dict],
    log_status: Callable
):
    """
    Credential context manager that does nothing.

    This can used when no credentials are included.
    """
    yield
