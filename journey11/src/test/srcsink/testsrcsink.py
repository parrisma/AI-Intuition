from typing import List

from journey11.src.interface.srcsink import SrcSink
from src.interface.capability import Capability
from src.interface.notification import Notification


class TestSrcSinkGood(SrcSink):

    def __init__(self):
        super().__init__()
        return

    def __call__(self, *args, **kwargs):
        return

    @property
    def name(self) -> str:
        return "DummyName"

    @property
    def topic(self) -> str:
        return "DummyTopic"

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
