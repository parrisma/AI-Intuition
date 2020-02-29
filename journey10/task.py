from abc import ABC, abstractmethod
from journey10.state import State


class Task(ABC):
    @abstractmethod
    @property
    def id(self) -> int:
        """
        The globally unique id of the task.
        :return: task id as int
        """
        pass

    @abstractmethod
    @property
    def state(self) -> State:
        """
        Current State of the Task
        :return: Current state
        """
        pass

    @abstractmethod
    @state.setter
    def state(self,
              s: State) -> None:
        """
        Set the tasks new state
        :param s: the state to set the task to
        """
        pass

    @abstractmethod
    @property
    def start_state(self) -> State:
        """
        The start state for the given task
        :return: The start state
        """
        pass

    @abstractmethod
    @property
    def terminal_state(self) -> State:
        """
        The terminal (end) state for the task
        :return: The terminal (end) state
        """
        pass

    @abstractmethod
    def do_work(self,
                work: int) -> int:
        """
        Do the given units of work, i.e. decrement the number of work units from the residual effort remaining
        for the task. If the number of work units is greater than the residual then the difference of work
        units is 'lost' as the task will absorb any additional.
        :param work: The number of units of work to do.
        :return: The remaining units of work, where 0 means the task ne
        """
        pass
