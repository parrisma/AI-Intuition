from abc import abstractmethod
import inspect
import threading
import logging
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.workrequest import WorkRequest
from journey11.src.interface.worknotification import WorkNotification
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.state import State


class TaskPool(SrcSink):
    class PubNotification:
        pass

    def __init__(self):
        """
        Check this or child class has correctly implemented callable __call__ as needed to handle both the
        PubSub listener events and the work timer events.
        """
        super().__init__()
        self._call_lock = threading.Lock()
        return

    def __del__(self):
        try:
            self._call_lock.release()
        except:
            pass
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
        elif isinstance(arg1, WorkNotification):
            self._put_task(arg1)
        elif isinstance(arg1, TaskPool.PubNotification):
            self._do_pub(arg1)
        else:
            msg = "Unexpected type [{}] passed to {}.__call__".format(type(arg1), self.__class__.__name__)
            logging.critical(msg)
            raise ValueError(msg)
        return

    @purevirtual
    @abstractmethod
    def _put_task(self,
                  work_initiate: WorkNotification) -> None:
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
    def _do_pub(self,
                pub_notification: 'TaskPool.PubNotification') -> None:
        """
        Check for any pending tasks and advertise or re-advertise them on the relevant topic
        :param pub_notification: The publication notification closure
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
