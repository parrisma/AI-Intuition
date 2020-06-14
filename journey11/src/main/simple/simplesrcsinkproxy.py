from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.srcsinkproxy import SrcSinkProxy


class SimpleSrcSinkProxy(SrcSinkProxy):
    # Annotation
    _name: str
    _topic: str

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
        else:
            self._name = None
            self._topic = None
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

    def _as_str(self) -> str:
        return "SimpleSrcSinkProxy for SrcSink: {} listening on Topic: {}".format(self._name, self._topic)

    def __repr__(self):
        return self._as_str()

    def __str__(self):
        return self._as_str()

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self.topic)
        return self._hash

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._name == other._name and self._topic == other._topic
