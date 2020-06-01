
import logging
import re

from typing import List, Optional, Type

from qtoggleserver.core import ports as core_ports
from qtoggleserver.lib import onewire


logger = logging.getLogger(__name__)


class DallasTemperatureSensor(onewire.OneWirePeripheral):
    TEMP_PATTERN = r't=(\d+)'
    ERROR_VALUE = '85000'  # This value indicates a communication error

    logger = logger

    def __init__(self, **kwargs) -> None:
        self._temp: Optional[float] = None

        super().__init__(**kwargs)

    def make_port_args(self) -> List[Type[core_ports.BasePort]]:
        from .ports import Temperature

        return [
            Temperature
        ]

    def get_temp(self) -> Optional[float]:
        data = self.read()
        if data:
            m = re.search(self.TEMP_PATTERN, data, re.MULTILINE | re.DOTALL)
            if m:
                value_str = m.group(1)
                if value_str == self.ERROR_VALUE:
                    raise core_ports.PortReadError('Sensor communication error')

                self._temp = round(int(value_str) / 100.0) / 10.0
                self.debug('temperature is %.1f degrees', self._temp)

        return self._temp
