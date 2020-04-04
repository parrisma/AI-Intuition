from journey11.src.interface.srcsink import SrcSink


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
