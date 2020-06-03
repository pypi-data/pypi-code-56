# -*- coding: utf-8 -*-
"""Account class module for HekrAPI"""
__all__ = [
    'Account',
]
import logging
from json import JSONDecodeError, loads
from typing import Dict, Optional, Tuple

from aiohttp import ClientSession

from .const import DEFAULT_APPLICATION_ID
from .device import Device, CloudConnector
from .exceptions import AccountUnauthenticatedException, AccountDevicesUpdateFailedException, HekrAPIException, HekrValueError

_LOGGER = logging.getLogger(__name__)


class Account:
    """Account class for HekrAPI

    Raises:
        ValueError: Account constructor is not provided possible ways to authenticate
        AccountUnauthenticatedException: Account did not authenticate prior to calling method

    Attributes:
        __username (str): Account username
        __password (str, optional): Account password (not required with token)
        __access_token (str, optional): Authentication 'Bearer' token (not required with password)
        __refresh_token (str, optional): Refresh token (not required with password)
        __devices (dict): Dictionary with 'Device' objects belonging to account
        application_id (str): Application ID (has default value)
    """

    AUTH_URL = 'https://uaa-openapi.hekr.me/login'
    BASE_URL = 'https://user-openapi.hekreu.me'

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None,
                 access_token: Optional[str] = None, refresh_token: Optional[str] = None,
                 application_id: str = DEFAULT_APPLICATION_ID, reauth_on_fail: bool = True):
        # @TODO: refactor after enabling authentication support
        if not access_token and not (username and password):
            raise HekrAPIException("At least one authentication method (token, username/password) must be set up")

        self.application_id = application_id

        self.__username = username
        self.__password = password
        self.__access_token = access_token
        self.__refresh_token = refresh_token

        self.expires_at = None
        self._user_id = None

        self.reauth_on_fail = reauth_on_fail

        self.__connectors = {}

        self.__devices: Dict[str, Device] = {}

    def get_connector(self, connect_host: str, connect_port: int = 186):
        if not self.__access_token:
            raise AccountUnauthenticatedException(account=self)

        key = (connect_host, connect_port)
        if key not in self.__connectors:
            connector = CloudConnector(
                token=self.__access_token,
                connect_host=connect_host,
                connect_port=connect_port,
                application_id=self.application_id
            )
            self.__connectors[key] = connector
            return connector
        return self.__connectors[key]

    @property
    def connectors(self) -> Dict[Tuple[str, int], CloudConnector]:
        return self.__connectors

    @property
    def devices(self) -> Dict[str, Device]:
        """Device dictionary accessor

        Returns:
            Dict[str, Device] -- dictionary of devices (device_id => Device object)
        """
        return self.__devices

    def _generate_auth_header(self):
        if not self.__access_token:
            raise AccountUnauthenticatedException(account=self)
        return {'Authorization': 'Bearer ' + self.__access_token}

    async def refresh_authentication(self, refresh_token: Optional[str] = None):
        """ Refresh authentication manually. """
        if refresh_token is None:
            refresh_token = self.__refresh_token
        if refresh_token is None:
            raise HekrValueError('refresh_token', 'None', 'refresh token')

    async def authenticate(self, pid='00000000000', client_type='ANDROID', app_version='1.0.0:0', app_name="hekrapi"):
        """Authenticate account with Hekr"""
        from datetime import datetime, timedelta
        if self.__refresh_token:
            if datetime.now() < self.expires_at:
                if await self.refresh_authentication():
                    return True

        _LOGGER.debug('Initiating authentication session for account %s' % self)
        async with ClientSession() as session:
            payload = {
                'username': self.__username,
                'password': self.__password,
                'pid': pid,
                'clientType': client_type,
                'appLoginInfo': {
                    "id": self.application_id,
                    "os": 9,
                    "type": "hekrapi",
                    "appVersion": app_version,
                    "name": "hekrapi",
                }
            }
            _LOGGER.debug('Sending request payload to %s for account %s' % (self.AUTH_URL, self))
            async with session.post(self.AUTH_URL, json=payload) as response:
                response = await response.json()
                # @TODO: Exception handling probably required
                access_token = response.get('access_token')
                if access_token:
                    # Succesful response
                    _LOGGER.info('Successful login for account %s' % self)
                    self.__access_token = access_token
                    self.__refresh_token = response.get('refresh_token')
                    
                    # @TODO: research 'token_type' response
                    self._user_id = response['user']
                    self.expires_at = datetime.now() + timedelta(seconds=response['expires_in'])

                    return True
                
                _LOGGER.error('Failed to authenticate account %s' % self)
                return False

    async def get_devices(self) -> Dict[str, dict]:
        auth_header = self._generate_auth_header()
        base_url_devices = self.BASE_URL + '/devices?size={}&page={}'

        request_devices = 20
        current_page = 0

        devices_info = dict()
        async with ClientSession() as session:
            more_devices = True
            while more_devices:
                request_url = base_url_devices.format(
                    request_devices,
                    current_page
                )

                async with session.get(request_url, headers=auth_header) as response:
                    content = await response.read()
                    _LOGGER.debug('Received response (%d) for account %s: %s' % (response.status, self, content))
                    try:
                        response_list = loads(content)
                    except JSONDecodeError:
                        raise AccountDevicesUpdateFailedException(account=self,
                                                                  response=response,
                                                                  reason='Received non-JSON response')

                    if response.status != 200:
                        await session.close()
                        reason = 'Account credentials incorrect' if response.status in (401, 403) \
                            else 'Unknown HTTP error'
                        raise AccountDevicesUpdateFailedException(account=self, response=response, reason=reason)

                    more_devices = (len(response_list) == request_devices)

                    devices_info.update({
                        device_info['devTid']: device_info
                        for device_info in response_list
                    })

        return devices_info

    async def update_devices(self, devices_info: Optional[Dict[str, dict]] = None) -> Dict[str, Device]:
        """
        Get devices, and update attributes if an object already exists, or create new ones based on retrieved info.
        :return: Dictionary with new devices indexed by device ID
        """

        if devices_info is None:
            devices_info = await self.get_devices()

        devices = {}
        for device_id, device_attributes in devices_info:
            if device_id in self.__devices:
                self.__devices[device_id].device_info = device_attributes
            else:
                device = Device(device_id=device_id, control_key=device_attributes['ctrlKey'])
                device.connector = self.get_connector(connect_host=device_attributes['dcInfo']['connectHost'])

                devices[device_id] = device

        if devices:
            self.__devices.update(devices)

        return devices
