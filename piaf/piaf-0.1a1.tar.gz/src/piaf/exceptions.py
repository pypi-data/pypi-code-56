# coding: utf-8
"""Define all exceptions that are used in the piaf framework."""
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    import piaf.agent  # noqa
    import piaf.platform as plt  # noqa

__all__ = [
    "InvalidStateException",
    "StateTransitionException",
    "UnsupportedOperationException",
    "MessageNotSentException",
]


class InvalidStateException(Exception):
    """
    Exception raised when an operation cannot be performed because of an invalid state.

    The exception message contains the state and the operation that was attempted.
    """

    def __init__(
        self,
        state: Union["piaf.agent.AgentState", "plt.PlatformState"],
        operation: str = "",
    ):
        """
        Create a new :class:`InvalidStateException`.

        :param state: object's state when the exception occurred.
        :param operation: the operation that was attempted when the exception occurred.
        """
        super().__init__(f"Cannot perform operation {operation} when state is {state}.")


class StateTransitionException(Exception):
    """
    Exception raised when the object can't transition from a state to another.

    The exception's message contains the original state and the state that was targeted.
    """

    def __init__(
        self,
        from_: Union["piaf.agent.AgentState", "plt.PlatformState"],
        to: Union["piaf.agent.AgentState", "plt.PlatformState"],
    ):
        """
        Create a new :class:`StateTransitionException`.

        :param from_: the object's state
        :param to_: the state that can't be reached
        """
        super().__init__(f"Cannot transition from state {from_} to state {to}.")


class UnsupportedOperationException(Exception):
    """
    Exception raised when the requested operation is not supported.

    The message can provide extra information about the reasons.
    """

    def __init__(self, msg: str = ""):
        """
        Create a new :class:`UnsupportedOperationException`.

        :param msg: why this operation is not supported (optional)
        """
        super().__init__(msg)


class MessageNotSentException(Exception):
    """Raised when something went wrong and a message sending failed."""

    def __init__(self):
        """Create a new :class:`MessageNotSentException`."""
        super().__init__(
            "Your message couldn't be sent, see MTS logs for more information."
        )
