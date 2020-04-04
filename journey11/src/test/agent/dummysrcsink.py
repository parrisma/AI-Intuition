from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.uniquetopic import UniqueTopic


class DummySrcSink(SrcSink):

    def __init__(self, name: str):
        self._name = name
        self._topic = UniqueTopic().topic()
        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic
