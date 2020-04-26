import threading


class CountDownBarrier:
    def __init__(self,
                 barrier_count: int):
        self._barrier_count = barrier_count
        self._lock = threading.RLock()
        self._sem = threading.Semaphore()
        self._sem.acquire(blocking=False)
        return

    def decr(self):
        with self._lock:
            self._barrier_count = max(0, self._barrier_count - 1)
        if self._barrier_count == 0:
            self._sem.release()

    def wait(self):
        self._sem.acquire(blocking=True)
        return
