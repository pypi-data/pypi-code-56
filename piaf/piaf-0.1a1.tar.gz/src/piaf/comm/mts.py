# coding: utf-8
"""
This module contains every related to the Message Transport System.

The MTS is seperated in different components:

* :class:`MessageTransferHandler`, which are components designed to handle
  communication using a specific protocol
* :class:`PlayloadParser`, which are responsible to dump and load
  :class:`piaf.comm.ACLMessage`
* the :class:`MTS` component, which provide a common interface for agents

class:`MessageTransferHandler` and class:`PlayloadParser` are interfaces that allow
you to create your own components (and thus use your own transport protocol or playload
representation).

The only implemented class:`MessageTransferHandler` is the
class:`MemoryMessageTransferHandler`, which uses the program's memory to transfer
messages. This handler can only work for agents running on the same platform.
"""
import abc
import threading
import logging
import copy

import asyncio
import piaf.exceptions as ex
import piaf.comm

from typing import ClassVar, Dict, Type, Any, Optional, Union

__all__ = [
    "MemoryMessageTransferHandler",
    "MessageTransferHandler",
    "MTS",
    "PlayloadParser",
]


class _MailBox:
    """Agent's mailbox."""

    def __init__(self):
        """Create a new mailbox."""
        self._queue = []
        self._sync = asyncio.Condition()

    async def get(
        self, template: "piaf.comm.MessageTemplate" = piaf.comm.MT_ALL()
    ) -> "piaf.comm.ACLMessage":
        """
        Retrieve the first matching message in the mail box.

        This method blocks until such message is inserted with the method :meth:`put`.
        Note that the mesage is removed from the queue so two successive calls to
        :meth:`get` (or :meth:`get_nowait`) will end up with two different messages.
        """
        async with self._sync:
            for i in range(len(self._queue)):
                if template.apply(self._queue[i]):
                    return self._queue.pop(i)
            while True:
                await self._sync.wait()
                if template.apply(self._queue[-1]):
                    return self._queue.pop(-1)

    async def get_nowait(
        self, template: "piaf.comm.MessageTemplate" = piaf.comm.MT_ALL()
    ) -> Union[None, "piaf.comm.ACLMessage"]:
        """
        Retrieve the first matching message in the mail box.

        Unlike :meth:`get`, this method returns ``None`` if no matching message is
        found. Otherwise, the behavior is similar to :meth:`get`.
        """
        async with self._sync:
            for i in range(len(self._queue)):
                if template.apply(self._queue[i]):
                    return self._queue.pop(i)
        return None

    async def put(self, item: "piaf.comm.ACLMessage") -> None:
        """Put the provided message in this mailbox."""
        async with self._sync:
            self._queue.append(item)
            self._sync.notify_all()


class PlayloadParser(metaclass=abc.ABCMeta):
    """Abstract playload parser. Use concrete classes to load or dump playload."""

    _PARSERS: ClassVar[Dict[str, Type["PlayloadParser"]]] = {}
    _COMPONENT_NAME: ClassVar[str] = ""

    def __init_subclass__(cls, cmp_name: str):
        super().__init_subclass__()
        PlayloadParser._PARSERS[cmp_name] = cls
        cls._COMPONENT_NAME = cmp_name

    @classmethod
    def get_parser(cls, cmp_name: str):
        return cls._PARSERS[cmp_name]

    @abc.abstractmethod
    def dump(self, data: Any, encoding: str = "utf-8") -> bytearray:
        """Dump the provided data into a :class:`bytearray`.

        :param data: the playload to dump
        :param encoding: how string are encoded
        :return: the playload dumped into the bytearray
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, data: bytearray, encoding: str = "utf-8") -> Any:
        """Load a playload from the provided bytearray.

        :param data: the bytearray
        :param encoding: how strings are encoded
        :return: a playload
        """
        raise NotImplementedError()


class Singleton(type):
    """
    Metaclass designed to implement the singleton pattern.

    Threadsafety is garanteed.
    """

    _instance: Optional["Singleton"] = None
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class MTS:
    """
    MTS is the Message Transport System of the Agent Platform.

    It provides a public interface for all existing agent, allowing them to send and
    receive messages from other agents. THe MTS can handle several protocols using
    different schemes (http, memory, ftp ...)
    """

    def __init__(self):
        """Create a new MTS."""
        super().__init__()
        self._agt_mapping = {}
        self.logger: logging.Logger = logging.getLogger(type(self).__name__)
        self._handlers = {}

    @property
    def schemes(self):
        """Get the supported protocols."""
        return self._handlers.keys()

    async def add_address(self, scheme: str, agent: "piaf.comm.AID") -> str:
        """
        Request a new address for an agent.

        :param scheme: the scheme (http, smtp ...)
        :param agent: the agent this address will be bounded
        :raise ValueError: the scheme is not supported by this MTF
        """
        # Get the handler associated to the provided scheme
        handler = None
        try:
            handler = self._handlers[scheme]
        except KeyError:
            raise ValueError(f"{scheme} is not supported by this MTS")

        # Get agent queue or create one
        queue = self._agt_mapping.setdefault(agent, _MailBox())

        # Request a new address
        address = await handler.create_address(agent, queue)

        return address

    async def remove_address(self, scheme: str, agent: "piaf.comm.AID") -> None:
        """
        Remove a mapping between an agent and a scheme.

        Raise an error if the mapping doesn't exists.

        :param scheme: the scheme (http, smtp ...)
        :param agent: the agent in the mapping
        """
        # Get the handler associated to the provided scheme
        handler = None
        try:
            handler = self._handlers[scheme]
        except KeyError:
            raise ValueError(f"{scheme} is not supported by this MTS")

        await handler.delete_address(agent)

    async def send(self, message: "piaf.comm.ACLMessage") -> None:
        """
        Send the given message.

        :param message: The message that should be sent.
        :raise UnsupportedOperationException: if the receiver is None
        :raise ex.MessageNotSentException: if the MTS did not succeed sending the
                                           message
        :raise TypeError: if the receiver has a wrong type
        """
        if message.receiver is None:
            raise ex.UnsupportedOperationException(
                "Broadcasting is currently not supported"
            )

        elif isinstance(message.receiver, piaf.comm.AID):
            msg_sent = False
            for address in message.receiver.addresses:
                scheme = address.split(":")[0]
                try:
                    await self._handlers[scheme].send(message)
                except Exception as e:
                    self.logger.warning(
                        "Failed sending a message to %s: ", address, exc_info=e
                    )
                else:
                    msg_sent = True
                    break
            if not msg_sent:
                raise ex.MessageNotSentException()

        elif isinstance(message.receiver, (list, tuple, set, frozenset)):
            for receiver in message.receiver:
                cpy = copy.deepcopy(message)
                cpy.receiver = receiver
                await self.send(cpy)

        else:
            raise TypeError(
                "Message receiver should be either None, an AID or a Sequence of AIDs."
            )

    async def receive(
        self,
        agent: "piaf.comm.AID",
        template: "piaf.comm.MessageTemplate" = piaf.comm.MT_ALL(),
    ) -> "piaf.comm.ACLMessage":
        """
        Retrieve the first message matching the template.

        If no template is provided, match the first message. Be advise that this is
        blocking call, meaning it won't return until a matching message is found.

        :param agent: the identity of the calling agent
        :param template: the template used to retrieve the messages
        """
        queue: _MailBox = self._agt_mapping[agent]
        return await queue.get(template)

    async def receive_nowait(
        self,
        agent: "piaf.comm.AID",
        template: "piaf.comm.MessageTemplate" = piaf.comm.MT_ALL(),
    ) -> Union[None, "piaf.comm.ACLMessage"]:
        """
        Retrieve the first message matching the template.

        If no template is provided, match the first message. If no message matches the
        template, this will return None.

        :param agent: the identity of the calling agent
        :param template: the template used to retrieve the messages
        """
        queue: _MailBox = self._agt_mapping[agent]
        return await queue.get_nowait(template)

    def install_handler(self, handler: "MessageTransferHandler"):
        """
        Install a new :class:`MessageTransfertHandler` to this MTS.

        The MTS will accept this handler only if the scheme is not handled yet.

        :param handler: the handler to install
        :raise Exception: the protocol is already managed by another handler.
        """
        scheme = handler.scheme
        if scheme in self._handlers:
            raise Exception()  # TODO: raise better exception

        self._handlers[scheme] = handler


class MessageTransferHandler(metaclass=abc.ABCMeta):
    """The message transfer handler."""

    SCHEME = ""

    @abc.abstractmethod
    async def send(self, message: "piaf.comm.ACLMessage") -> None:
        """
        Send the provided message.

        It is assumed that the receiver has one address using this handler protocol.

        :param message: the message to send.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def create_address(self, agent: "piaf.comm.AID", queue: _MailBox) -> str:
        """
        Create a new address for the provided agent.

        The provided mailbox will be used to put incoming messages.

        :param agent: the agent that will have a new address
        :param queue: the mailbox where to put incoming messages
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_address(self, agent: "piaf.comm.AID") -> None:
        """
        Delete the agent's address.

        It doesn't remove it from the :class:`piaf.comm.AID`.

        :param agent: the agent the address belongs to
        """
        raise NotImplementedError()

    @property
    def scheme(self):
        """Get the protocol's scheme handled by this handler."""
        return self.SCHEME


class MemoryMessageTransferHandler(MessageTransferHandler):
    """Use RAm to transfer messages. Only works for platform-internal destinations."""

    SCHEME = "memory"

    def __init__(self):
        super().__init__()
        self._mapping: Dict["piaf.comm.AID", _MailBox] = {}

    async def send(self, message: "piaf.comm.ACLMessage") -> None:
        assert isinstance(message.receiver, piaf.comm.AID)
        r_agent = message.receiver
        await self._mapping[r_agent].put(message)

    async def create_address(self, agent: "piaf.comm.AID", queue: _MailBox) -> str:
        address = f"memory://{agent.hap_name}/{agent.short_name}"
        self._mapping[agent] = queue
        return address

    async def delete_address(self, agent: "piaf.comm.AID") -> None:
        del self._mapping[agent]
