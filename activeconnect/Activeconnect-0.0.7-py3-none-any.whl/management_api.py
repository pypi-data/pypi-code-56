import urllib
from urllib.request import Request
from urllib.error import HTTPError

import logging

import json
from Activeconnect.config import ACTIVE_CONNECT_SERVER
from Activeconnect.hmac import make_authentication_headers

import enum

logger = logging.getLogger("activeconnect")


class ManagementAPIResult(enum.IntEnum):
    success = 0
    failed = 1
    user_exists = 2
    has_mobile_device = 3
    no_mobile_device = 4


class ManagementAPI:
    """
        Wrapper class for the Activeconnect management REST API.

        Attributes:
            application_id (str): The application id of the Activeconnect application.
            application_secret (str): The application secret of the Activeconnect application.
    """

    def __init__(self, application_id: str, application_secret: str):
        """
            The constructor for ManagementAPI class.

            Parameters:
                application_id (str): The application id of the Activeconnect application.
                application_secret (str): The application secret of the Activeconnect application.
        """
        self.application_id = application_id
        self.application_secret = application_secret

    def add_users(self, users: [str]):
        """
            Registers users with Activeconnect.

            Calls the Activeconnect service to register users.

            Parameters:
            users ([str]): An array containing the user IDs to add.
            .

            Returns:
            created([str]), existing([str]): created is an array containing the users that were registered.
                                             existing is an array containing any users that already existed.
                                             If the method fails the return value us None,None.

            """
        if users is None:
            raise ValueError("users cannot be None")

        url = "{}/management/add_users/{}".format(ACTIVE_CONNECT_SERVER, self.application_id)

        headers = make_authentication_headers(self.application_id, self.application_secret, url)

        headers["Content-Type"] = "application/json"

        body = json.dumps({"users": users}).encode('UTF-8')

        req = urllib.request.Request(url, headers=headers, data=body)

        try:
            add_users_response = urllib.request.urlopen(req)

            if 200 <= add_users_response.code < 300:
                d = add_users_response.read()
                response_data = json.loads(d)
                status = response_data.get("status")

                if not status:
                    logger.debug("Failed to add users status == False")
                    return None, None

                new_users = None
                existing_users = None
                user_data = response_data.get('users')
                if user_data is not None:
                    new_users = user_data.get('created')
                    existing_users = user_data.get('existing')
                    logger.debug("Users added {} existing {}".format(new_users, existing_users))
                else:
                    logger.debug("Failed to add users - unexpected response data.")

                return new_users, existing_users
        except HTTPError as ex:
            logger.warning("Failed to add users {}".format(ex))

        return None, None

    def add_user(self, user: str):
        """
            Registers a single with Activeconnect.

            Calls the Activeconnect service to register a single user

            Parameters:
            user (str): The user IDs to add.
            .

            Returns:
            ManagementAPIResult: ManagementAPIResult.success if the method succeeds.
                                 ManagementAPIResult.user_exists if the user already exists.
                                 ManagementAPIResult.failed if the method failed.

            """
        users = [user]
        new_users, existing_users = self.add_users(users)

        if existing_users is not None and len(existing_users) != 0:
            return ManagementAPIResult.user_exists
        if new_users is None or len(new_users) == 0:
            return ManagementAPIResult.failed

        return ManagementAPIResult.success

    def delete_users(self, user_ids: [str]):
        """
            Deletes users from Activeconnect.

            Calls the Activeconnect service to delete users

            Parameters:
            user_ids ([str]): The user IDs to delete.
            .

            Returns:
            ManagementAPIResult: ManagementAPIResult.success if the method succeeds.
                                 ManagementAPIResult.failed if the method fails.

            """

        url = "{}/management/delete_users/{}".format(ACTIVE_CONNECT_SERVER, self.application_id)

        headers = make_authentication_headers(self.application_id, self.application_secret, url)

        headers["Content-Type"] = "application/json"

        body = json.dumps({"users": user_ids}).encode('UTF-8')

        req = urllib.request.Request(url, headers=headers, data=body)

        try:
            active_connect_response = urllib.request.urlopen(req)
            d = active_connect_response.read()
            response_data = json.loads(d)
            status = response_data.get("status")

            if not status:
                logger.debug("Failed to delete users status == False")
                return ManagementAPIResult.failed

            return ManagementAPIResult.success

        except HTTPError as ex:
            logger.warning("Failed to delete users {}".format(ex))
            return ManagementAPIResult.failed

    def delete_user(self, user_id: str):
        """
            Deletes a single from Activeconnect.

            Calls the Activeconnect service to delete a single user

            Parameters:
            user_id (str): The user ID to delete.
            .

            Returns:
            ManagementAPIResult: ManagementAPIResult.success if the method succeeds.
                                 ManagementAPIResult.failed if the method fails.

            """
        return self.delete_users([user_id])

    def get_registration_link(self, user_id: str, display_name: str):
        """
            Gets a device registration link for the specified user.

            Calls the Activeconnect service to obtain a device registration for a user.
            The registration link is intended to be called from a mobile application to register a particular device.

            Parameters:
            user_id (str): The user ID.
            display_name (str): Activeconnect does not store personal user information. The display_name parameter
                                allows activeConnect to generate a device registration link that includes a displayable
                                name for the user.
            .

            Returns:
            registration url (str): A device registration URL that can be used to register a physical device
                                    with activeConnect.
                                    None if the method fails.

            """
        if user_id is None or len(user_id) == 0:
            raise ValueError("user_id cannot be None")

        encoded_user = urllib.parse.quote_plus(user_id)

        display_name_query = ""

        if display_name is not None and len(display_name) > 0:
            encoded_display_name = urllib.parse.quote_plus(display_name)
            display_name_query = "?display_name={}".format(encoded_display_name)

        url = "{}/management/device_registration_link/{}/{}{}".format(ACTIVE_CONNECT_SERVER,
                                                                      self.application_id,
                                                                      encoded_user,
                                                                      display_name_query)

        headers = make_authentication_headers(self.application_id, self.application_secret, url)

        req = urllib.request.Request(url, headers=headers)

        try:
            active_connect_response = urllib.request.urlopen(req)

            if 200 <= active_connect_response.code < 300:
                d = active_connect_response.read()
                response_data = json.loads(d)

                status = response_data.get("status")

                if not status:
                    logger.debug("Failed to get registration link response status == False")
                    return None

                registration_url = response_data.get('register_url')
                return registration_url
        except HTTPError as ex:
            logger.warning("Failed to get registration link {}".format(ex))
            return None
        return None

    def send_registration_sms(self, user_id: str, display_name: str, phone_number: str, message):
        """
            Sends a device registration SMS to the specified user using the specified phone number.

            Parameters:
            user_id (str): The user ID.
            display_name (str): Activeconnect does not store personal user information. The display_name parameter
                                allows activeConnect to generate a device registration link that includes a displayable
                                name for the user.
            phone_number (str): The phone number to send the link to including country code +1XXXYYYZZZZ
            message (str): Optional message body - the link is appended to the message.

            Returns:
            result (bool): True if the message was sent.

        """
        if user_id is None or len(user_id) == 0:
            raise ValueError("user_id cannot be None")

        if phone_number is None or len(phone_number) == 0:
            raise ValueError("phone_number cannot be None")

        encoded_user = urllib.parse.quote_plus(user_id)

        payload = {"phone_number": phone_number}

        if display_name is not None:
            payload["display_name"] = display_name

        if message is not None:
            payload["message"] = message

        body = json.dumps(payload).encode('UTF-8')

        url = "{}/management/send_registration_sms/{}/{}".format(ACTIVE_CONNECT_SERVER,
                                                                 self.application_id,
                                                                 encoded_user)

        headers = make_authentication_headers(self.application_id, self.application_secret, url)
        headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, headers=headers, data=body)

        try:
            active_connect_response = urllib.request.urlopen(req)
            if 200 <= active_connect_response.code < 300:
                d = active_connect_response.read()
                response_data = json.loads(d)

                status = response_data.get("status")

                if not status:
                    logger.debug("Failed to send registration SMS {}".format(response_data.get("reason")))
                return status
        except HTTPError as ex:
            logger.warning("Failed to send registration SMS {}".format(ex))
        return False

    def has_registered_mobile_device(self, user_id: str):
        """
            Checks to see if the specified user has registered a mobile device.

            Parameters:
            user_id (str): The user ID.
            .

            Returns:
            mobile device (ManagementAPIResult): has_mobile_device if the user has a mobile device.
                                                 no_mobile_device if the user has no mobile device
                                                 failed if the method fails.

        """
        if user_id is None or len(user_id) == 0:
            raise ValueError("user_id cannot be None")

        encoded_user = urllib.parse.quote_plus(user_id)

        url = "{}/management/has_registered_mobile_device/{}/{}".format(ACTIVE_CONNECT_SERVER,
                                                                        self.application_id,
                                                                        encoded_user)

        headers = make_authentication_headers(self.application_id, self.application_secret, url)

        req = urllib.request.Request(url, headers=headers)

        try:
            active_connect_response = urllib.request.urlopen(req)

            if 200 <= active_connect_response.code < 300:
                d = active_connect_response.read()
                response_data = json.loads(d)

                device_registered = response_data.json.get("device_registered")

                if device_registered is None:
                    return ManagementAPIResult.failed

                return ManagementAPIResult.has_mobile_device if device_registered else ManagementAPIResult.no_mobile_device

        except HTTPError as ex:
            logger.warning("Failed to get registration link {}".format(ex))

        return ManagementAPIResult.failed
