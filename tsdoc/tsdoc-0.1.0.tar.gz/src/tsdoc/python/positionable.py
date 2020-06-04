from textx.model import get_model


class Positionable:
    def linecol(self):
        return get_model(self)._tx_parser.pos_to_linecol(self._tx_position)

    def line(self):
        return self.linecol()[0]

    def column(self):
        return self.linecol()[1]
