import httpx
import xml.etree.ElementTree as ElementTree
import datetime


class Apex(object):
    """
    Abstracts the interaction with the Neptune Apex Aquacontroller.
    Allows querying of current probe and outlet states as well as control
    of individual outlets.
    """

    def __init__(self, ip_address, user='admin', password='1234'):
        self.ip_address = ip_address
        self._user = user
        self._password = password

        # set/updated on calls to :fetch_current_state
        self.hostname = None
        self.serial = None
        self.timezone = None
        self.date = None
        self.probes = {}
        self.outlets = {}

    async def validate_connection(self):
        """ Attempts to connect to the configured server, returns one of:
        success, cannot_connect, invalid_auth """
        # noinspection PyBroadException
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://%s/nstatus.sht" % self.ip_address,
                                            auth=(self._user, self._password))
        except Exception:
            return 'cannot_connect'
        if response.status_code == 401:
            return 'invalid_auth'
        if response.status_code == 200:
            return 'success'
        return 'unknown:' + response.status_code

    @staticmethod
    def __safe_node_get_text(node):
        if node is None:
            return None
        return node.text

    async def fetch_current_state(self):
        """
        Connect to the Apex and pull down/refresh all information. New probes/outlets will be
        added. Renamed entries will not be detected, the legacy names will persist until
        recreation of Apex object. Holding a reference to a probe or outlet and calling this
        method will result in the state of that item being updated. Can raise an ApexException
        if there is an issue communicating with the Apex.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://%s/cgi-bin/status.xml" % self.ip_address,
                                            auth=(self._user, self._password))
            self._parse_xml_state(response.content)
        except Exception as e:
            raise ApexException from e
        return None

    def _parse_xml_state(self, xml_string):
        """ Parses the xml returned by the Apex into Probes and Outlets, does the actual
        work of fetch_current_state() """
        xml = ElementTree.fromstring(xml_string)
        self.hostname = xml.find('hostname').text
        self.serial = xml.find('serial').text
        self.timezone = xml.find('timezone').text
        self.date = datetime.datetime.strptime(xml.find('date').text, '%m/%d/%Y %H:%M:%S')

        probes = xml.find('probes')
        for probe_xml in probes:
            probe_name = probe_xml.find('name').text
            probe = self.probes.get(probe_name, Probe(
                probe_xml.find('name').text,
                self.__safe_node_get_text(probe_xml.find('type'))
            ))
            probe.value = float(probe_xml.find('value').text)
            self.probes[probe_name] = probe

        outlets = xml.find('outlets')
        for outlet_xml in outlets:
            outlet_name = outlet_xml.find('name').text
            outlet = self.outlets.get(outlet_name, Outlet(
                outlet_xml.find('name').text,
                outlet_xml.find('outputID').text,
                outlet_xml.find('deviceID').text
            ))
            outlet.state = outlet_xml.find('state').text
            self.outlets[outlet_name] = outlet

        return None

    async def update_outlet(self, outlet):
        """ Connect to the Apex and set the given outlet's state. Currently only supports non-profile
        states, so ON, OFF, and AUTO. Can raise an ApexException if there is an issue communicating
        with the Apex."""
        assert type(outlet) is Outlet, "outlet is not an Outlet instance: %r" % outlet
        state_id = 0  # Default to 'AUTO'
        if not outlet.is_auto():
            if outlet._get_on_off() == 'OFF':
                state_id = 1
            else:
                state_id = 2

        payload = {
            'Update': 'Update',
            'noResponse': 0,
            outlet.name + '_state': state_id
        }
        async with httpx.AsyncClient() as client:
            try:
                await client.post("http://%s/status.sht" % self.ip_address,
                                  auth=(self._user, self._password),
                                  data=payload)
            except Exception as e:
                raise ApexException() from e


class Probe(object):
    """
    Apex probe. Usually but not always has a type of one of:
    Temp, pH, ORP, Amps, Cond
    Could also have others if one has additional equipment. Feel free
    to submit an example status.xml if you are seeing other values.
    Flow meters do not include a type value, and will have a None type.
    """

    def __init__(self, name, type):
        self.name = name
        self.type = type


class Outlet(object):
    """
    Apex outlet. Has four binary? statuses, which are ON, OFF, AUTO-ON and
    AUTO-OFF, and arbitrary profiles to support dimming/speed controlled devices.
    When putting an outlet into AUTO mode, you do not specify what state
    it will set to, so the class state goes to UNKNOWN (neither on or off) until
    the Apex status is refetched.
    """

    def __init__(self, name, output_id, device_id):
        self.name = name
        self.output_id = output_id
        self.state = 'UNKNOWN'
        self.state_known = False
        self.device_id = device_id

    def is_auto(self):
        """ :return true if the outlet is currently set to AUTO mode. """
        return self.state in ['AON', 'AOF', 'AUTO']

    def enable_auto(self):
        """ sets this outlet to auto mode, which invalidates the current on/off status until refetched. """
        self.state = 'AUTO'

    def is_on(self):
        """ :return true if the outlet is not forced off (OFF) and not automatically off (AOF). ON, AON,
        and any analog profile other than 'AUTO' will be treated as truthy for is_on.
        Immediately after enabling auto mode via :py:meth:enable_auto(), and until data is refetched,
        outlet will return false for both is_on() and is_off()."""
        return self.state not in ['OFF', 'AOF', 'AUTO']

    def is_off(self):
        """ :return true if the outlet has been forced off, or if in auto mode and it was off at
        last update. Immediately after enabling auto mode, and until data is refetched, outlet
        will return false for both is_on() and is_off()."""
        return self.state in ['AOF', 'OFF']

    def force_on(self):
        """ Forces the outlet on, disabling auto mode. """
        self.state = 'ON'

    def force_off(self):
        """ Forces the outlet off, disabling auto mode. """
        self.state = 'OFF'


class ApexException(Exception):
    """Generic exception to wrap any network/parse issues talking to Apex"""
    pass
