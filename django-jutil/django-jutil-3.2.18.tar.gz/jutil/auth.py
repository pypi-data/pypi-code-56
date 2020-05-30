from typing import Optional

from django.contrib.auth.models import User
from rest_framework.exceptions import NotAuthenticated
from rest_framework.request import Request


def require_auth(request: Request, exceptions: bool = True) -> Optional[User]:
    """
    Returns authenticated User.
    :param request: HttpRequest
    :param exceptions: Raise (NotAuthenticated) exception. Default is True.
    :return: User
    """
    if not request.user or not request.user.is_authenticated:
        if exceptions:
            raise NotAuthenticated()
        return None
    return request.user


class AuthUserMixin:
    @property
    def auth_user(self) -> User:
        """
        Returns authenticated user.
        :return: User
        """
        return require_auth(self.request, exceptions=True)  # type: ignore
