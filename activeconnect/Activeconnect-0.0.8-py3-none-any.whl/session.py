import urllib
from urllib.request import Request
from urllib.error import HTTPError
import json
import logging
from dataclasses import field
from marshmallow_dataclass import dataclass
from Activeconnect.status import Status
from Activeconnect.hmac import make_authentication_headers

logger = logging.getLogger("activeconnect")

@dataclass
class Session:
    """
        Represents an Activeconnect session.

        Attributes:

            authenticated (bool): True if the authentication request was successful (does not indicate authentication status).
            failure_reason (str): If authenticated is False indicates the reason for failure.
            session_status (Status): The status of the session - a value of Session.pending indicates authentication is in progress.
            session_token (str): Identifies the session.
            session_secret (str): Secret used to authenticate REST calls to Activeconnect service.
            status_url (str): The URL to call to get the status of the session.
            logout_url (str): The URL to call to destroy the session.

    """

    @property
    def failed(self):
        return self.session_status in [Status.failed, Status.timeout, Status.cancelled]

    @property
    def in_progress(self):
        return self.session_status in [Status.pending,Status.identifying]

    @property
    def active(self):
        return self.session_status == Status.active

    def __init__(self, session_status: Status, session_token: str, session_secret: str,
                 logout_url: str, status_url: str, failure_reason: str = None):
        self.session_status = session_status
        self.failure_reason = failure_reason
        self.session_token = session_token
        self.session_secret = session_secret
        self.status_url = status_url
        self.logout_url = logout_url

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Session):
            return  self.session_status == other.session_status and \
                    self.failure_reason == other.failure_reason and \
                    self.session_token == other.session_token and \
                    self.session_secret == other.session_secret and \
                    self.status_url == other.status_url and \
                    self.logout_url == other.logout_url
        return False

    @staticmethod
    def from_authentication_response(session_data: dict):
        """
            Creates a Session from the response to an authentication request.

            Parameters:
                session_data (dict): The data returned from a call to the Activeconnect authenticate_user API.
        """
        authentication_status = session_data.get("authentication_status")

        if authentication_status is None:
            raise ValueError("session_data does not contain the authentication_status key")

        authenticated = authentication_status.get("authenticated")

        session_status = Status[authentication_status["session_status"]] if authenticated else Status.failed
        failure_reason = None if authenticated else authentication_status["reason"]
        session_token = authentication_status["session_token"] if authenticated else None
        session_secret = authentication_status["session_secret"] if authenticated else None
        status_url = authentication_status["status_url"] if authenticated else None
        logout_url = authentication_status["logout_url"] if authenticated else None

        return Session(session_status=session_status, session_token=session_token, session_secret=session_secret,
                       logout_url=logout_url, status_url=status_url, failure_reason=failure_reason)

    session_token: str = field(metadata={"required": False, "allow_none": True})
    session_secret: str = field(metadata={"required": False, "allow_none": True})
    logout_url: str = field(metadata={"required": False, "allow_none": True})
    status_url : str = field(metadata={"required": False, "allow_none": True})
    failure_reason: str = field(metadata={"required": False, "allow_none": True})
    session_status: Status = field(metadata={"required": True})

    def get_status(self ):
        """
            Get the status of the session.

            Calls the Activeconnect service to get the status of the session.

            Returns:
            Status: The status of the session.

            """

        headers = make_authentication_headers(client_id=self.session_token,
                                                   client_shared_secret=self.session_secret,
                                                   request_uri=self.status_url)
        headers["Content-Type"] = "application/json"

        req = urllib.request.Request(self.status_url, headers=headers, method='GET')

        try:
            auth_response = urllib.request.urlopen(req)
            if 200 <= auth_response.code < 300:
                d = auth_response.read()
                j = json.loads(d)
                auth_status = j.get('authentication_status')
                self.session_status = Status[auth_status['session_status']]
                return self.session_status
        except HTTPError as ex:
            logger.warning("get status failed {}".format(ex))
        return Status.failed

    def destroy(self):
        """
            Terminates the session.

            Calls the Activeconnect service to terminate this session.

            Returns:
            Boolean: True of the session was destroyed otherwise False.

            """

        headers = make_authentication_headers(client_id=self.session_token,
                                                   client_shared_secret=self.session_secret,
                                                   request_uri=self.logout_url)
        headers["Content-Type"] = "application/json"

        req = urllib.request.Request(self.logout_url, headers=headers, method='POST')

        try:
            destroy_response = urllib.request.urlopen(req)
            if 200 <= destroy_response.code < 300:
                body = destroy_response.read()
                j = json.loads(body)

                destroyed = j.get('status')

                if destroyed is None:
                    destroyed = False

                return destroyed
        except HTTPError as ex:
            logger.warning("destroy session failed {}".format(ex))

        return False
