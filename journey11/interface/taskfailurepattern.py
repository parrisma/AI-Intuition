from abc import ABC, abstractmethod
from journey11.lib.state import State
from journey11.lib.purevirtual import purevirtual


class TaskFailurePattern(ABC):
    @purevirtual
    @abstractmethod
    def failure_adjusted_state(self,
                               original_state: State) -> State:
        """
        At the failure rate return a state that is before the supplied original_state else return the original_state
        as supplied.
        :param original_state: The state the task will transition to assuming the task does not fail according to the
        failure pattern
        :return: The state the task should transition to according to the failure pattern.
        """
        pass

    @property
    @purevirtual
    @abstractmethod
    def failure_rate(self) -> float:
        """
        The rate at which tasks fail.
        :return: The failure rate 0.0 to 1.0
        """
        pass
