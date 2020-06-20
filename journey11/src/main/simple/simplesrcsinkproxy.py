from typing import List
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.srcsinkproxy import SrcSinkProxy
from journey11.src.interface.capability import Capability
from journey11.src.main.simple.simplecapability import SimpleCapability


class SimpleSrcSinkProxy(SrcSinkProxy):
    # Annotation
    _name: str
    _topic: str
    _capabilities: List[SimpleCapability]

    def __init__(self,
                 srcsink: SrcSink = None):
        """
        A Proxy Object to bew sent over the wire as identification and basic meta data of a source sink.
        Default construction is allowed but only supported for use with the proto-buf serialization.
        :param srcsink:
        """
        super().__init__()
        if srcsink is not None:
            self._name = srcsink.name
            self._topic = srcsink.topic
            self._capabilities = srcsink.capabilities
        else:
            self._name = None
            self._topic = None
            self._capabilities = None
        return

    @property
    def name(self) -> str:
        """
        The unique name of the SrcSink
        :return: The SrcSink name
        """
        return self._name

    @property
    def topic(self) -> str:
        """
        The unique topic name that SrcSink listens on for activity specific to it.
        :return: The topic
        """
        return self._topic

    @property
    def capabilities(self) -> List[Capability]:
        """
        The capabilities of the SrcSink
        :return: A List of the SrcSink's capabilities
        """
        return self._capabilities

    def _as_str(self) -> str:
        return "SimpleSrcSinkProxy for SrcSink: {} listening on Topic: {}".format(self._name, self._topic)

    def __repr__(self):
        return self._as_str()

    def __str__(self):
        return self._as_str()

    def __hash__(self):
        if self._hash is None:
            self._hash = hash("{}-{}".format(self.name, self.topic))
        return self._hash

    def __eq__(self, other):
        if isinstance(other, self.__class__) and self._name == other._name and self._topic == other._topic:
            for c1, c2 in zip(self._capabilities, other._capabilities):
                if c1 != c2:
                    return False
        return True
