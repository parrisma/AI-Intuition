import logging
import threading
import random
import time
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.countdownbarrier import CountDownBarrier


class SyncMultiThread:
    global_id = 0

    def __init__(self,
                 num_tests: int,
                 count_down_barrier: CountDownBarrier):
        self.ctb = count_down_barrier
        self.num_tests = num_tests
        self._lock = threading.RLock()
        self.res = 0

        for _ in range(self.num_tests):
            self._incr()
            threading.Timer((random.random() * 5), self, args=[SyncMultiThread.global_id]).start()
            SyncMultiThread.global_id += 1
        return

    def _incr(self):
        with self._lock:
            self.res += 1

    def _decr(self):
        with self._lock:
            self.res -= 1

    def __call__(self, thread_id):
        logging.info("Start work for thread {}".format(thread_id))
        time.sleep(random.random() * 2)
        self._decr()
        self.ctb.decr()
        logging.info("Done work for thread {}".format(thread_id))
        return

    @property
    def counter(self) -> int:
        return self.res


if __name__ == "__main__":
    LoggingSetup()
    ntests = 50
    ctb = CountDownBarrier(ntests)
    ttc = SyncMultiThread(count_down_barrier=ctb, num_tests=ntests)
    logging.info("Waiting for all")
    ctb.wait()
    logging.info("All done")
    assert ttc.res == 0
