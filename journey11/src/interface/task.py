from abc import ABC, abstractmethod
from journey11.src.lib.purevirtual import purevirtual
from journey10.lib.state import State


class Task(ABC):
    @property
    @abstractmethod
    @purevirtual
    def id(self) -> int:
        """
        The globally unique id of the task.
        :return: task id as int
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def lead_time(self) -> State:
        """
        The lead time between task starting and task finishing
        :return: Lead Time
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def state(self) -> State:
        """
        Current State of the Task
        :return: Current state
        """
        pass

    @state.setter
    @abstractmethod
    @purevirtual
    def state(self,
              s: State) -> None:
        """
        Set the tasks new state
        :param s: the state to set the task to
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def failed(self) -> bool:
        """
        True if task filed during processing
        :return: Failure state of task
        """
        pass

    @failed.setter
    @abstractmethod
    @purevirtual
    def failed(self,
               s: bool) -> None:
        """
        Set the failed status of the task
        :param s: the state to set the task to
        """
        pass

    @abstractmethod
    @purevirtual
    def do_work(self,
                work: int) -> int:
        """
        Do the given units of work, i.e. decrement the number of work units from the residual effort remaining
        for the task. If the number of work units is greater than the residual then the difference of work
        units is 'lost' as the task will absorb any additional.
        :param work: The number of units of work to do.
        :return: The remaining units of work, where 0 means the task is complete in it's current state.
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def work_in_state_remaining(self) -> int:
        """
        The units of work required to complete the current state
        :return: The units of work remaining in the current state
        """
        pass

    @classmethod
    @abstractmethod
    @purevirtual
    def process_start_state(cls,
                            start_state: State = None) -> State:
        pass

    @classmethod
    @abstractmethod
    @purevirtual
    def process_end_state(cls,
                          end_state: State = None) -> State:
        pass

    @abstractmethod
    @purevirtual
    def reset(self) -> None:
        """
        Return the Task to the same state at which it was constructed
        """
        pass
