import numpy as np
from typing import List
from journey11.src.interface.srcsink import SrcSink
from src.interface.capability import Capability
from src.interface.notification import Notification
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.namegen.namegen import NameGen
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.test.gibberish.gibberish import Gibberish


class TestSrcSink(SrcSink):
    # Annotation
    _name: str
    _topic: str

    def __init__(self):
        super().__init__()
        self._name = NameGen.generate_random_name()
        self._topic = "topic={}".format(UniqueRef().ref)
        self._capabilities = self._random_capabilities()
        return

    def __call__(self, *args, **kwargs):
        return

    def _random_capabilities(self):
        """
        Generate up to 10 random capabilities
        :return: List of upto 10 random capabilities
        """
        capabilities = list()
        for _ in range(np.random.randint(low=1, high=10, size=1)[0]):
            capabilities.append(SimpleCapability(uuid=UniqueRef().ref, capability_name=Gibberish.word_gibber()))
        return capabilities

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def capabilities(self) -> List[Capability]:
        return list()

    def _do_srcsink_ping_notification(self, ping_notification: Notification) -> None:
        raise NotImplementedError("Method not implemented on this TEST class")

    def _do_srcsink_ping(self, ping_request: Notification) -> None:
        raise NotImplementedError("Method not implemented on this TEST class")

    def get_address_book(self) -> List['SrcSink']:
        raise NotImplementedError("Method not implemented on this TEST class")

    def _update_address_book(self, srcsink: 'SrcSink') -> None:
        raise NotImplementedError("Method not implemented on this TEST class")
