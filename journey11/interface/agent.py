from abc import ABC, abstractmethod
from journey10.lib.state import State
from pubsub import pub
from journey11.interface.taskpool import TaskPool


class Agent(ABC):
    class AgentPubExceptionHandler(pub.IListenerExcHandler):
        def __call__(self, listener_id, topic_obj):
            print("Agent Id [{}] raised an exception".format(listener_id))
            return

    def __init__(self):
        # Register PubSub exception handler.
        pub.setListenerExcHandler(Agent.AgentPubExceptionHandler())

        # Check child class implements callable with correct signature as is required to be a subscription
        # target
        cl = getattr(self, "__call__", None)
        if not callable(cl):
            raise NotImplemented("Must implement __call__(self, arg1)")
        return

    @abstractmethod
    def __call__(self, arg1):
        if self._id == "3":
            raise Exception("Test Exception")
        print("Listener [{}] - Message: {}".format(self._id, arg1))
        return

    @abstractmethod
    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        pass

    # ----- P R O P E R T I E S -----

    @property
    @abstractmethod
    def capacity(self) -> int:
        """
        The current work capacity of the actor.
        :return: Current work capacity as int
        """
        pass

    @property
    @abstractmethod
    def from_state(self) -> State:
        """
        The state the actor expects to receive tasks in
        :return: from state
        """
        pass

    @property
    @abstractmethod
    def to_state(self) -> State:
        """
        The state the actor will process tasks into
        :return: to state
        """
        pass

    @property
    @abstractmethod
    def failure_rate(self) -> float:
        """
        The rate at which completed tasks fail.
        :return: Failure state of the actor
        """
        pass

    @failure_rate.setter
    @abstractmethod
    def failure_rate(self,
                     f: bool) -> None:
        """
        The rate at which completed tasks fail.
        :param f: the failure state of the actor
        """
        pass
