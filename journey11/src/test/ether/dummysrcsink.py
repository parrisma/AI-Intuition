from typing import Iterable
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.capability import Capability
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.lib.simplecapability import SimpleCapability


class DummySrcSink(SrcSink):
    _glob_id = 1

    def __init__(self):
        self._name = "{}-{}-{}".format(DummySrcSink.__class__.__name__, DummySrcSink.global_id(), UniqueRef())
        self._topic = UniqueTopic.topic(prefix=DummySrcSink.__class__.__name__)
        self._capabilities = [SimpleCapability("DummyCapability")]

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

    @classmethod
    def global_id(cls) -> str:
        gid = str(cls._glob_id)
        cls._glob_id += 1
        return gid

    @property
    def capabilities(self) -> Iterable[Capability]:
        """
        The collection of capabilities of the SrcSink
        :return: The collection of capabilities
        """
        return self._capabilities
