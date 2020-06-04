from textx.model import get_model
from typing import cast
from typing import Tuple


class Positionable:
    _tx_position: int

    @property
    def linecol(self) -> Tuple[int, int]:
        return cast(
            Tuple[int, int],
            get_model(self)._tx_parser.pos_to_linecol(self._tx_position),
        )

    @property
    def line(self) -> int:
        return self.linecol[0]

    @property
    def column(self) -> int:
        return self.linecol[1]
