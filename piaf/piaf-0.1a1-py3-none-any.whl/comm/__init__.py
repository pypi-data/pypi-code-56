# coding: utf-8
"""
This module contains the building blocks of Agent Communication.

The first block is the agent identity, called :class:`AID`. It is unique to each agent.
Then comes :class:`ACLMessage` and templates.
"""

import datetime
import logging
import enum
import copy
import abc
import functools
import operator

from typing import Sequence, MutableMapping, Union, Any, Type


__all__ = [
    "AID",
    "Performative",
    "ACLMessage",
    "MessageTemplate",
    "MT_ALL",
    "MT_AND",
    "MT_OR",
    "MT_PERFORMATIVE",
    "MT_SENDER",
    "MT_CONVERSATION_ID",
    "MT_ENCODING",
    "MT_IN_REPLY_TO",
    "MT_LANGUAGE",
    "MT_ONTOLOGY",
    "MT_PROTOCOL",
    "MT_REPLY_TO",
    "MT_REPLY_WITH",
]


class AID:
    """
    Represents the identification of an agent.

    This class has three fields:

    * ``name``, which is mandatory and has the following form: agent_name@hap_name
    * ``addresses``, which is a list of URLs to reach the agent. This field is optional
      and URL order is relevant as it defines priorities between URLs.
    * ``resolvers``, which is a list of AIDs of name resolvers agents. This field is
      optional and order is relevant as it defines priorities between AIDs.

    According to the the fipa standard, two AIDs are considered equivalent if their
    ``name`` parameters are the same. Full specification is available here:
    http://www.fipa.org/specs/fipa00023/.
    """

    def __init__(
        self, name: str, addresses: Sequence[str] = (), resolvers: Sequence["AID"] = ()
    ):
        """
        Create a new AID object.

        The create object will be initialized with the provided values. The
        ``name`` parameter must following this format : agent@hap_name.

        :param name: the agent's name
        :param addresses: an ordered sequence of URLs.
        :param resolvers: an ordered sequence of AIDs.
        :raise ValueError: if the name parameter is not well formed
        """
        if name is None or "@" not in name:
            raise ValueError("fullname must be agent_name@hap_name")

        self._name: str = name
        self.addresses: Sequence[str] = list(addresses)
        self.resolvers: Sequence["AID"] = list(resolvers)

    @property
    def short_name(self) -> str:
        """Short agent's name (ie the part before '@' in the name)."""
        return self._name.split("@")[0]

    @property
    def hap_name(self) -> str:
        """Host agent plateform name (ie the part after '@' in the name)."""
        return self._name.split("@")[1]

    @property
    def name(self) -> str:
        """Agent's name."""
        return self._name

    def __eq__(self, value: Any) -> bool:
        """Two AIDs are equal if and only if their name are the same."""
        return (
            value is not None
            and type(value) == type(self)
            and self._name == value._name
        )

    def __hash__(self):
        return hash(self.name)

    def __deepcopy__(self, memo):
        return AID(self.name, tuple(self.addresses), tuple(self.resolvers))


class Performative(enum.Enum):
    """
    Performatives available as defined in http://www.fipa.org/specs/fipa00037/.

    These performatives are intended to be used with :class:`ACLMessage`. Here is
    a small summary of what each performative means:

    **ACCEPT_PROPOSAL**
        The action of accepting a previously submitted proposal to perform an action.
    **AGREE**
        The action of agreeing to perform some action, possibly in the future.
    **CANCEL**
        The action of one agent informing another agent that the first agent no longer
        has the intention that the second agent perform some action.
    **CFP**
        The action of calling for proposals to perform a given action.
    **CONFIRM**
        The sender informs the receiver that a given proposition is true, where the
        receiver is known to be uncertain about the proposition.
    **DISCONFIRM**
        The sender informs the receiver that a given proposition is false, where the
        receiver is known to believe, or believe it likely that, the proposition is
        true.
    **FAILURE**
        The action of telling another agent that an action was attempted but the
        attempt failed.
    **INFORM**
        The sender informs the receiver that a given proposition is true.
    **INFORM_IF**
        A macro action for the agent of the action to inform the recipient whether or
        not a proposition is true.
    **INFORM_REF**
        A macro action for sender to inform the receiver the object which corresponds
        to a descriptor, for example, a name.
    **NOT_UNDERSTOOD**
        The sender of the act (for example, i) informs the receiver (for example, j)
        that it perceived that j performed some action, but that i did not understand
        what j just did. A particular common case is that i tells j that i did not
        understand the message that j has just sent to i.
    **PROPAGATE**
        The sender intends that the receiver treat the embedded message as sent
        directly to the receiver, and wants the receiver to identify the agents denoted
        by the given descriptor and send the received propagate message to them.
    **PROPOSE**
        The action of submitting a proposal to perform a certain action, given certain
        preconditions.
    **PROXY**
        The sender wants the receiver to select target agents denoted by a given
        description and to send an embedded message to them.
    **QUERY_IF**
        The action of asking another agent whether or not a given proposition is true.
    **QUERY_REF**
        The action of asking another agent for the object referred to by a referential
        expression.
    **REFUSE**
        The action of refusing to perform a given action, and explaining the reason for
        the refusal.
    **REJECT_PROPOSAL**
        The action of rejecting a proposal to perform some action during a negotiation.
    **REQUEST**
        The sender requests the receiver to perform some action. One important class of
        uses of the request act is to request the receiver to perform another
        communicative act.
    **REQUEST_WHEN**
        The sender wants the receiver to perform some action when some given
        proposition becomes true.
    **REQUEST_WHENEVER**
        The sender wants the receiver to perform some action as soon as some
        proposition becomes true and thereafter each time the proposition becomes true
        again.
    **SUBSCRIBE**
        The act of requesting a persistent intention to notify the sender of the value
        of a reference, and to notify again whenever the object identified by the
        reference changes.
    """

    def _generate_next_value_(name, start, count, last_values):  # noqa
        return name.lower().replace("_", "-")

    ACCEPT_PROPOSAL = enum.auto()
    AGREE = enum.auto()
    CANCEL = enum.auto()
    CFP = enum.auto()
    CONFIRM = enum.auto()
    DISCONFIRM = enum.auto()
    FAILURE = enum.auto()
    INFORM = enum.auto()
    INFORM_IF = enum.auto()
    INFORM_REF = enum.auto()
    NOT_UNDERSTOOD = enum.auto()
    PROPAGATE = enum.auto()
    PROPOSE = enum.auto()
    PROXY = enum.auto()
    QUERY_IF = enum.auto()
    QUERY_REF = enum.auto()
    REFUSE = enum.auto()
    REJECT_PROPOSAL = enum.auto()
    REQUEST = enum.auto()
    REQUEST_WHEN = enum.auto()
    REQUEST_WHENEVER = enum.auto()
    SUBSCRIBE = enum.auto()


class ACLMessage:
    """
    Representation of an ACL Message as described in
    http://www.fipa.org/specs/fipa00061/.

    Add more here.
    """

    class Builder:
        """
        Ease :class:`ACLMessage` creation.

        It also perform some checks when the message is built. When building a message,
        you must:

        * Instantiate a new builder
        * use :meth:`performative` to set the message performative
        * use whatever method to fill the message
        * invoke the :meth:`build` method

        Calling twice the same method will override the previously set value.
        """

        def __init__(self):
            """Create a new :class:`ACLMessage.Builder`."""
            self._params: MutableMapping[str, Any] = {}
            self.logger: logging.Logger = logging.getLogger(ACLMessage.Builder.__name__)

        def performative(self, value: Union[str, Performative]) -> "ACLMessage.Builder":
            """Set the message performative."""
            self._params["performative"] = value
            return self

        def sender(self, value: AID) -> "ACLMessage.Builder":
            """Set the message sender."""
            self._params["sender"] = value
            return self

        def receiver(self, value: Union[AID, Sequence[AID]]) -> "ACLMessage.Builder":
            """Set the message receiver."""
            self._params["receiver"] = value
            return self

        def reply_to(self, value: AID) -> "ACLMessage.Builder":
            """Set the reply_to field."""
            self._params["reply_to"] = value
            return self

        def content(self, value: Any) -> "ACLMessage.Builder":
            """Set the message content."""
            self._params["content"] = value
            return self

        def language(self, value: str) -> "ACLMessage.Builder":
            """Set the message language."""
            self._params["language"] = value
            return self

        def encoding(self, value: str) -> "ACLMessage.Builder":
            """Set the message encoding."""
            self._params["encoding"] = value
            return self

        def ontology(self, value: str) -> "ACLMessage.Builder":
            """Set the message ontology."""
            self._params["ontology"] = value
            return self

        def protocol(self, value: str) -> "ACLMessage.Builder":
            """
            Set the message protocol.

            When set, you should also set the conversation-id and the reply-by fields.
            Otherwise, it will emit a warning.
            """
            self._params["protocol"] = value
            return self

        def conversation_id(self, value: str) -> "ACLMessage.Builder":
            """Set the message conversation id."""
            self._params["conversation_id"] = value
            return self

        def reply_with(self, value: str) -> "ACLMessage.Builder":
            """Set the reply_with field."""
            self._params["reply_with"] = value
            return self

        def in_reply_to(self, value: str) -> "ACLMessage.Builder":
            """Set the in_reply_to field."""
            self._params["in_reply_to"] = value
            return self

        def reply_by(self, value: datetime.datetime) -> "ACLMessage.Builder":
            """Set the reply_by field."""
            self._params["reply_by"] = value
            return self

        def custom(self, key: str, value: Any) -> "ACLMessage.Builder":
            """
            Add a custom field to the message.

            According to FIPA specification, the key should start with "X-". This
            method will automatically add the prefix if it is not set.

            :param key: the key to identify the custom field
            :param value: the value stored in the field
            """
            if not key.startswith("X-"):
                key = "X-" + key
            self._params[key] = value
            return self

        def build(self) -> "ACLMessage":
            """
            Build the message.

            Also perform some sanity checks

            :raise ValueError: if the performative field is not set
            """
            # Perform some checks
            self._check_performative()
            self._check_protocol()
            return ACLMessage(**self._params)

        def _check_performative(self):
            if "performative" not in self._params:
                raise ValueError("performative must be set")

        def _check_protocol(self):
            if "protocol" not in self._params:
                self.logger.warning("Not using a protocol is not recommended.")
            else:
                if "conversation_id" not in self._params:
                    self.logger.warning(
                        "When using a protocol, conversation-id should be defined."
                    )
                if "reply_by" not in self._params:
                    self.logger.warning(
                        "When using a protocol, reply-by should be defined."
                    )

    def __init__(
        self,
        performative: Union[str, Performative],
        sender: AID = None,
        receiver: Union[AID, Sequence[AID]] = None,
        reply_to: AID = None,
        content: Any = None,
        language: str = None,
        encoding: str = None,
        ontology: str = None,
        protocol: str = None,
        conversation_id: str = None,
        reply_with: str = None,
        in_reply_to: str = None,
        reply_by: datetime.datetime = None,
        **kwargs: Any,
    ):
        """
        Create a new :class:`ACLMessage`.

        Unless you know what you are doing, use the :class:`ACLMessage.Builder` class
        instead.
        """
        self.performative = performative
        self.sender = sender
        self.receiver = receiver
        self.reply_to = reply_to
        self.content = content
        self.language = language
        self.encoding = encoding
        self.ontology = ontology
        self.protocol = protocol
        self.conversation_id = conversation_id
        self.reply_with = reply_with
        self.in_reply_to = in_reply_to
        self.reply_by = reply_by

        self.__dict__.update(kwargs)

    def __deepcopy__(self, memo) -> "ACLMessage":
        """Make a deep copy of this ACLMessage."""
        args = {}
        for attribute in self.__dict__:
            args[attribute] = copy.deepcopy(self.__dict__[attribute], memo)

        return type(self)(**args)


class MessageTemplate(abc.ABC):
    """Common interface for filtering messages."""

    @abc.abstractmethod
    def apply(self, message: ACLMessage) -> bool:
        """
        Apply the template to the provided message.

        :param message: the message to check
        """
        raise NotImplementedError()


class MT_OR(MessageTemplate):
    """Complex template that do a logic "OR" using the provided templates."""

    def __init__(self, a: MessageTemplate, b: MessageTemplate, *args):
        """
        Create a new OR message template with the provided message templates.

        You must provide at least two of them.

        :param a: the first message template
        :param b: the second message template
        :param args: any number of additional message templates
        """
        self._filters = [a, b] + list(args)

    def apply(self, message):
        return functools.reduce(operator.or_, (f.apply(message) for f in self._filters))


class MT_AND(MessageTemplate):
    """Complex template that do a logic "AND" using the provided templates."""

    def __init__(self, a: MessageTemplate, b: MessageTemplate, *args):
        self._filters = [a, b] + list(args)

    def apply(self, message):
        """
        Create a new AND message template with the provided message templates.

        You must provide at least two of them.

        :param a: the first message template
        :param b: the second message template
        :param args: any number of additional message templates
        """
        return functools.reduce(
            operator.and_, (f.apply(message) for f in self._filters)
        )


def _MT_factory(field_name: str) -> Type[MessageTemplate]:
    """
    Class factory used to create message templates matching simple message fields.

    :param field_name: the message field's name
    """

    def __init__(self, value: str):
        """
        Initializer for the class.

        :param value: the field's value
        """
        self._value = value

    def apply(self, message: ACLMessage) -> bool:
        return getattr(message, field_name) == self._value

    clazz = type(
        f"MT_{field_name.upper()}",
        (MessageTemplate,),
        {"__init__": __init__, "apply": apply},
    )
    return clazz


#: Check the performative field
MT_PERFORMATIVE = _MT_factory("performative")

#: Check the sender field
MT_SENDER = _MT_factory("sender")

#: Check the conversation_id field
MT_CONVERSATION_ID = _MT_factory("conversation_id")

#: Check the encoding field
MT_ENCODING = _MT_factory("encoding")

#: Check the in_reply_to field
MT_IN_REPLY_TO = _MT_factory("in_reply_to")

#: Check the language field
MT_LANGUAGE = _MT_factory("language")

#: Check the ontology field
MT_ONTOLOGY = _MT_factory("ontology")

#: Check the protocol field
MT_PROTOCOL = _MT_factory("protocol")

#: Check the reply_with field
MT_REPLY_WITH = _MT_factory("reply_with")

#: check the reply_to field
MT_REPLY_TO = _MT_factory("reply_to")


class MT_ALL(MessageTemplate):
    """Special template that matches all messages."""

    def apply(self, message):
        return True
