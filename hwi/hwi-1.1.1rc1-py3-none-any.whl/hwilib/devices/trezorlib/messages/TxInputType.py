# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .MultisigRedeemScriptType import MultisigRedeemScriptType

if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore


class TxInputType(p.MessageType):

    def __init__(
        self,
        address_n: List[int] = None,
        prev_hash: bytes = None,
        prev_index: int = None,
        script_sig: bytes = None,
        sequence: int = None,
        script_type: int = None,
        multisig: MultisigRedeemScriptType = None,
        amount: int = None,
        decred_tree: int = None,
        decred_script_version: int = None,
        prev_block_hash_bip115: bytes = None,
        prev_block_height_bip115: int = None,
    ) -> None:
        self.address_n = address_n if address_n is not None else []
        self.prev_hash = prev_hash
        self.prev_index = prev_index
        self.script_sig = script_sig
        self.sequence = sequence
        self.script_type = script_type
        self.multisig = multisig
        self.amount = amount
        self.decred_tree = decred_tree
        self.decred_script_version = decred_script_version
        self.prev_block_hash_bip115 = prev_block_hash_bip115
        self.prev_block_height_bip115 = prev_block_height_bip115

    @classmethod
    def get_fields(cls):
        return {
            1: ('address_n', p.UVarintType, p.FLAG_REPEATED),
            2: ('prev_hash', p.BytesType, 0),  # required
            3: ('prev_index', p.UVarintType, 0),  # required
            4: ('script_sig', p.BytesType, 0),
            5: ('sequence', p.UVarintType, 0),  # default=4294967295
            6: ('script_type', p.UVarintType, 0),  # default=SPENDADDRESS
            7: ('multisig', MultisigRedeemScriptType, 0),
            8: ('amount', p.UVarintType, 0),
            9: ('decred_tree', p.UVarintType, 0),
            10: ('decred_script_version', p.UVarintType, 0),
            11: ('prev_block_hash_bip115', p.BytesType, 0),
            12: ('prev_block_height_bip115', p.UVarintType, 0),
        }
