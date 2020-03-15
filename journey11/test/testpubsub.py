import threading
import time
from pubsub import pub


class ListenPayload:
    def __init__(self,
                 msg: str):
        self._msg = msg

    @property
    def msg(self) -> str:
        return self._msg


class TimerPayload:
    def __init__(self,
                 msg: str):
        self._msg = msg

    @property
    def msg(self) -> str:
        return self._msg


class Listener:
    _running = True

    @classmethod
    def running(cls, running: bool = None) -> bool:
        pv = cls._running
        if running is not None:
            cls._running = running
        return pv

    def __init__(self, listener_id: str):
        self._id = listener_id
        self._timer = None
        self.__timer_reset()
        return

    def __timer_reset(self) -> None:
        if Listener.running():
            self._timer = threading.Timer(1.0, self, args=[TimerPayload(self._id)]).start()
        return

    def __del__(self):
        if self._timer is not None:
            self._timer.cancel()
        pass

    def __call__(self, arg1):
        if isinstance(arg1, ListenPayload):
            self.do_listen_event(arg1.msg)
        elif isinstance(arg1, TimerPayload):
            self.do_timer_event(arg1.msg)
        else:
            raise ValueError("Unexpected type passed to {}.__call__ [{}]".format(self.__class__.__name__, type(arg1)))
        return

    def do_listen_event(self,
                        msg: str):
        if self._id == "3":
            raise Exception("Test Exception")
        print("Listener [{}] - Message: {}".format(self._id, msg))
        return

    def do_timer_event(self,
                       msg: str):
        print("Timer Message: {}".format(msg))
        self.__timer_reset()
        return


class ListenerExceptionHandler(pub.IListenerExcHandler):
    def __call__(self, listener_id, topic_obj):
        print("Listener [{}] raised an exception".format(listener_id))


pub.setListenerExcHandler(ListenerExceptionHandler())

if __name__ == "__main__":

    topic1 = "Topic1"
    topic2 = "Topic2"

    listeners = [Listener("1"),
                 Listener("2"),
                 Listener("3"),
                 Listener("4"),
                 Listener("5")]

    for listener in listeners:
        pub.subscribe(listener, topic1)

    for i in (0, -1):
        pub.subscribe(listeners[i], topic2)

    for i in range(5):
        pub.sendMessage(topicName=topic1, arg1=ListenPayload("T1-Msg-{}".format(i)))
        pub.sendMessage(topicName=topic2, arg1=ListenPayload("T2-Msg-{}".format(i)))
        time.sleep(1)

    Listener.running(False)
