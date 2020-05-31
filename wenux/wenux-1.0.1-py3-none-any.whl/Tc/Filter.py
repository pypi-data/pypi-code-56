import logging

from dataclasses import dataclass
from abc import abstractmethod

from Utils.Subprocess import check_call


class Filter(object):
    _flowid = ""
    @abstractmethod
    def _apply_filter(self, filter_list, ip_version, priority):
        pass

    @staticmethod
    def generate_filters(filter_list):
        filter_strings = []
        filter_strings_ipv6 = []

        for tc_filter in filter_list:
            filter_tokens = tc_filter.split(",")

            try:
                filter_string = ""
                filter_string_ipv6 = ""

                for token in filter_tokens:
                    token_split = token.split("=")
                    key = token_split[0]
                    value = token_split[1]

                    if key == "src" or key == "dst":
                        if "::" in value:
                            filter_string_ipv6 += f"match ip6 {key} {value} "
                        else:
                            filter_string += f"match ip {key} {value} "
                    else:
                        filter_string += f"match ip {key} {value} "
                        filter_string_ipv6 += f"match ip6 {key} {value} "
                    if key == "sport" or key == "dport":
                        filter_string += "0xffff "
                        filter_string_ipv6 += "0xffff "

            except IndexError:
                logging.error("Error: Invalid filter parameters")

            if filter_string:
                filter_strings.append(filter_string)
            if filter_string_ipv6:
                filter_strings_ipv6.append(filter_string_ipv6)

        return filter_strings, filter_strings_ipv6


@dataclass
class TcFilter(Filter):
    _ip: str = None
    _ipv6: str = None
    _nic: str = None
    _type: str = None
    _priority: int = 0

    def __post_init__(self):
        self._type_check(self._type)

        if self._type == "exclude":
            self._flowid = "1:2"
            self._priority = 1
            logging.debug(f"Excluding the following from network impairment:")
        else:
            self._flowid = "1:3"
            self._priority = 3
            logging.debug(f"Including the following for network impairment:")

        self._apply_filter(self._ip, "ip", self._priority)
        self._apply_filter(self._ipv6, "ipv6", self._priority+1)

    def _apply_filter(self, filter_list, ip_version, priority):
        for rule in filter_list:
            filter_cmd = f"tc filter add dev {self._nic} protocol {ip_version} " \
                         f"parent 1:0 prio {priority} u32 {rule}flowid {self._flowid}"
            check_call(filter_cmd)

    def _type_check(self, type):
        _allowed_types = ["include", "exclude"]
        if not (type in _allowed_types):
            raise Exception("Invalid type parameter")
        else:
            return
