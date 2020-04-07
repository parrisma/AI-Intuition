import logging
import threading
from journey11.src.lib.uniqueref import UniqueRef


class DummyCallable:
    def __init__(self):
        self._ref = UniqueRef().ref
        self._lock = threading.Lock()
        self._count = 0
        return

    def __call__(self, *args, **kwargs):
        with self._lock:
            self._count += 1
        logging.info("DummyCallable {} call method invocation {}".format(self._ref, self._count))
        return

    @property
    def invocation_count(self) -> int:
        return self._count

    def __str__(self):
        return "DummyCallable {} with invocation count {}".format(self._ref, self._count)

    def __repr__(self):
        return self.__str__()
