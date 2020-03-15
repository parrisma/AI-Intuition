from abc import ABC, abstractmethod
import threading


class A1(ABC):

    def __init__(self):
        print("A1.__init__ called")
        return

    @abstractmethod
    def am1(self):
        print("A1.am1 called")
        return


class A2(A1):

    def __init__(self):
        print("A2.__init__ called")
        super().__init__()
        self.lock = threading.Lock()
        self.res = 1

    @abstractmethod
    def am1(self):
        print("A2.am1 called")
        print("waiting")
        with self.lock:
            self.res += 1
            print("Done " + str(self.res))
        return


if __name__ == "__main__":
    pass
