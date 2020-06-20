import logging
import threading
import random
import time
from src.lib.aitrace.trace import Trace

num_tests = 500


class ThreadTestClass:
    global_id = 0

    def __init__(self):
        self.lock = threading.Lock()
        self.res = 0
        for _ in range(num_tests):
            threading.Timer((random.random() * .1), self, args=[ThreadTestClass.global_id]).start()
            ThreadTestClass.global_id += 1
        return

    def inc_counter(self):
        with self.lock:
            self.res += 1
            logging.info("Counter updated {}".format(self.res))
        return

    def __call__(self, thread_id):
        logging.info("Start work for thread {}".format(thread_id))
        self.inc_counter()
        logging.info("Done work for thread {}".format(thread_id))

    @property
    def counter(self) -> int:
        return self.res


if __name__ == "__main__":
    Trace()
    ttc = ThreadTestClass()
    time.sleep(5)
    assert (ttc.counter == num_tests)
