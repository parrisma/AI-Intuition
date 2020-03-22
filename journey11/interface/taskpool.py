from abc import ABC, abstractmethod
import inspect
from journey11.lib.purevirtual import purevirtual
from journey11.lib.state import State
from journey11.interface.srcsink import SrcSink
from journey11.interface.workrequest import WorkRequest
from journey11.interface.workinitiate import WorkInitiate


class TaskPool(SrcSink):

    def __init__(self):
        """
        Check this or child class has correctly implemented callable __call__ as needed to handle both the
        PubSub listener events and the work timer events.
        """
        cl = getattr(self, "__call__", None)
        if not callable(cl):
            raise NotImplemented("Must implement __call__(self, arg1)")
        else:
            # Check signature
            sig = inspect.signature(cl)
            if 'arg1' not in sig.parameters:
                raise NotImplemented("Must implement __call__(self, arg1)")
        return

    def __call__(self, arg1) -> None:
        """
        The agent is callable two contexts
        1. As the sink for PubSub in which case a TaskNotification will be passed
        2. As the handler for it's own timer to check if work needs to be done in which case WorkNotification is passed

        Other types for arg1 trigger a ValueError exception

        :param arg1: Either a TaskNotification or a WorkNotification
        """
        if isinstance(arg1, WorkRequest):
            self._get_task(arg1)
        elif isinstance(arg1, WorkInitiate):
            self._put_task(arg1)
        else:
            raise ValueError("Unexpected type [{}] passed to {}.__call__".format(type(arg1), self.__class__.__name__))
        return

    @purevirtual
    @abstractmethod
    def _put_task(self,
                  work_initiate: WorkInitiate) -> None:
        """
        Add a task to the task pool which will cause it to be advertised via the relevant topic unless the task
        is in it's terminal state.
        :param work_initiate: Details of the task being injected.
        """
        pass

    @purevirtual
    @abstractmethod
    def _get_task(self,
                  work_request: WorkRequest) -> None:
        """
        Send the requested task to the consumer if the task has not already been sent to a consumer
        :param work_request: The details of the task and the consumer
        """

    pass

    @purevirtual
    @abstractmethod
    def topic_for_state(self,
                        state: State) -> str:
        """
        The topic string on which tasks needing work in that state are published on
        :param state: The state for which the topic is required
        :return: The topic string for the given state
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def name(self) -> str:
        """
        The name of the task pool
        :return: The name of the task pool as string
        """
        pass
