# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json

import nbformat as nbf
from dial_core.notebook import NodeCells


class HyperparametersConfigNodeCells(NodeCells):
    """The HyperparametersConfigNodeCells class generates a block of code corresponding
    to the hyperparameters dictionary."""

    def _body_cells(self):
        value_cell = nbf.v4.new_code_cell(
            (
                f"{self.node.word_id()}.set_hyperparameters({self.node.inner_widget.get_hyperparameters()})"
            )
        )

        return [value_cell]
