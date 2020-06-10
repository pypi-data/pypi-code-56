from typing import Any

from jeffy.encoding import Encoding


class BytesEncoding(Encoding):
    """Bytes encoding class."""

    def encode(self, payload: Any) -> bytes:
        """
        Encode to bytes.

        Parameters
        ----------
        payload: Any

        Returns
        -------
        payload : bytes
        """
        return payload

    def decode(self, payload: bytes) -> Any:
        """
        Decode from bytes.

        Parameters
        ----------
        payload: bytes

        Returns
        -------
        payload : Any
        """
        return payload
