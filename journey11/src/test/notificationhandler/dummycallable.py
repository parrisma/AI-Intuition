import logging
import threading
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.notificationhandler import NotificationHandler


class DummyCallable:
    def __init__(self,
                 intial_interval: float = None,
                 max_interval: float = None,
                 with_back_off: bool = False):
        self._ref = UniqueRef().ref
        self._lock = threading.RLock()
        self._count = 0
        self._with_back_off = with_back_off
        self._initial_interval = intial_interval
        self._max_interval = max_interval
        return

    def __call__(self, *args, **kwargs):
        with self._lock:
            self._count += 1
        logging.info("DummyCallable {} call method invocation {}".format(self._ref, self._count))
        for arg in args:
            logging.info("DummyCallable arg: {}".format(arg))
        for key, value in kwargs.items():
            logging.info("DummyCallable kwarg: key {} value {}".format(key, value))

        new_interval = None
        if self._with_back_off:
            new_interval = NotificationHandler.back_off(reset=False,
                                                        curr_interval=args[0],
                                                        min_interval=self._initial_interval,
                                                        max_interval=self._max_interval,
                                                        factor=2)
        logging.info(
            "{} DummyCallable - back-off active - current interval {} new interval {}".format(self._count,
                                                                                              args[0], new_interval))
        return new_interval

    @property
    def invocation_count(self) -> int:
        return self._count

    def __str__(self):
        return "DummyCallable {} with invocation count {}".format(self._ref, self._count)

    def __repr__(self):
        return self.__str__()
