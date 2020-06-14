from typing import List
from journey11.src.interface.srcsink import SrcSink
from src.interface.capability import Capability
from src.interface.notification import Notification
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.namegen.namegen import NameGen


class TestSrcSink(SrcSink):
    # Annotation
    _name: str
    _topic: str

    def __init__(self):
        super().__init__()
        self._name = NameGen.generate_random_name()
        self._topic = "topic={}".format(UniqueRef().ref)
        return

    def __call__(self, *args, **kwargs):
        return

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

    def get_addressbook(self) -> List['SrcSink']:
        raise NotImplementedError("Method not implemented on this TEST class")

    def _update_addressbook(self, srcsink: 'SrcSink') -> None:
        raise NotImplementedError("Method not implemented on this TEST class")
