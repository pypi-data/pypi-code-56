"""
This module manage the context precision of calculations
using *affapy*.

Indeed, you can choice the precision using the **precision** class.
You can set different precision contexts between functions using the
precision decorator or use the class using the *with* statement.

This class changes the precision context of *mpmath*.

You can see **exPrecision1** and **exPrecision2** to see how it works.

"""

from contextlib import ContextDecorator
from mpmath import mp
from affapy.error import affapyError


class precision(ContextDecorator):
    """
    Manage precision for *affapy* library. You can use it:

    * As decorator of a function
    * Using the *with* statement

    It contains four fields:

    * **dps**: decimal precision (decimals number)
    * **prec**: binary precision (bits number)
    * **old_dps**: decimal precision before entry to the context
    * **old_prec**: binary precision before entry to the context

    **Example**:

    .. code-block:: python

        from affapy.precision import precision

        with precision(dps=30):
            x + y

        @precision(dps=30)
        def eval_fct(x, y):
            return x + y

    """

    def __init__(self, dps: int = None, prec: int = None):
        """
        Init the context manager for precision.
        You need to mention dps or prec. Both is useless.

        Args:
            dps (int): decimal precision of mpmath
            prec (int): binary precision of mpmath

        Raises:
            affapyError: Invalid value for precision

        """
        if isinstance(dps, int) or isinstance(prec, int):
            self._dps = dps
            self._prec = prec
        else:
            raise affapyError("Invalid value for precision")
        self._old_dps = None
        self._old_prec = None

    # Getter
    @property
    def dps(self):
        """
        Get decimal precision.
        """
        return self._dps

    @property
    def prec(self):
        """
        Get binary precision.
        """
        return self._prec

    @property
    def old_dps(self):
        """Get old decimal precision.
        """
        return self._old_dps

    @property
    def old_prec(self):
        """
        Get old binary precision.
        """
        return self._old_prec

    # Setter
    @dps.setter
    def dps(self, dps: int):
        """
        Set decimal precision.

        Args:
            dps (int): decimal precision

        """
        self._dps = dps
        mp.dps = dps

    @prec.setter
    def prec(self, prec: int):
        """
        Set binary precision.

        Args:
            prec (int): binary precision

        """
        self._prec = prec
        mp.prec = prec

    @old_dps.setter
    def old_dps(self, dps: int):
        """
        Set old decimal precision.

        Args:
            dps (int): decimal precision

        """
        self._old_dps = dps

    @old_prec.setter
    def old_prec(self, prec: int):
        """
        Set old binary precision.

        Args:
            prec (int): binary precision

        """
        self._old_prec = prec

    # Static Method - If you want to modify directly the precision
    @staticmethod
    def set_dps(dps: int):
        """
        Set decimal precision outside precision class.

        Args:
            dps (int): decimal precision

        """
        mp.dps = dps

    @staticmethod
    def set_prec(prec: int):
        """
        Set binary precision outside precision class.

        Args:
            prec (int): binary precision
        """
        mp.prec = prec

    def __enter__(self):
        """
        Set the *mpmath* precision for a portion of code.

        Raises:
            affapyError: No precision mentioned

        """
        self.old_dps, self.old_prec = mp.dps, mp.prec
        if self.dps is not None:
            mp.dps = self.dps
        elif self.prec is not None:
            mp.prec = self.prec
        else:
            raise affapyError("No precision mentioned")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Reset the *mpmath* precision to its last value.

        Raises:
            affapyError: No precision saved

        """
        if self.dps is not None:
            mp.dps = self.old_dps
        elif self.prec is not None:
            mp.prec = self.old_prec
        else:
            raise affapyError("No precision saved")
        return False
