import logging
import re
from typing import Optional

from django.http import HttpRequest
from jsm_user_services.support.local_threading_utils import add_to_local_threading
from jsm_user_services.support.local_threading_utils import remove_from_local_threading

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

logger = logging.getLogger(__name__)


class JsmJwtService(MiddlewareMixin):
    def process_request(self, request):
        add_to_local_threading("authorization_token", self._get_jwt_token_from_request(request))
        add_to_local_threading("user_ip", self._get_user_ip_from_request(request))

    def process_response(self, request, response):
        remove_from_local_threading("authorization_token")
        remove_from_local_threading("user_ip")
        return response

    @staticmethod
    def _get_jwt_token_from_request(request: HttpRequest) -> Optional[str]:
        """
        Extracts JWT token from a Django request object.
        """
        authorization_token = request.META.get("HTTP_AUTHORIZATION", "")

        match = re.match("Bearer", authorization_token)

        if not match:
            return None

        auth_type_beginning = match.span()[1]
        jwt_token = authorization_token[auth_type_beginning:].strip()

        return jwt_token

    @staticmethod
    def _get_user_ip_from_request(request: HttpRequest) -> Optional[str]:
        """
        Retrieve the user ip that made this request from Django HttpRequest object
        """
        return request.META.get("X-Original-Forwarded-For", None)
