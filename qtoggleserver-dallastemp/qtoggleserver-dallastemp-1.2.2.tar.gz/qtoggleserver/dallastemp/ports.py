
import logging

from typing import cast, Optional


from qtoggleserver.lib import onewire

from .dallastemperaturesensor import DallasTemperatureSensor


logger = logging.getLogger(__name__)


class Temperature(onewire.OneWirePort):
    TYPE = 'number'
    WRITABLE = False
    MIN = -55
    MAX = 125
    UNIT = u'\xb0C'  # Degrees celsius

    ID = 'temperature'

    async def read_value(self) -> Optional[float]:
        return cast(DallasTemperatureSensor, self.get_peripheral()).get_temp()
