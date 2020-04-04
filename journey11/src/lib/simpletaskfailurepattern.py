import numpy as np
from journey11.src.interface.taskfailurepattern import TaskFailurePattern
from journey11.src.lib.state import State


class SimpleTaskFailurePattern(TaskFailurePattern):

    def __init__(self,
                 failure_rate: float):
        self._failure_rate = failure_rate

    def failure_adjusted_state(self,
                               original_state: State) -> State:
        """
        At the failure rate return a state that is before the supplied original_state else return the original_state
        as supplied.
        :param original_state: The state the task will transition to assuming the task does not fail according to the
        failure pattern
        :return: The state the task should transition to according to the failure pattern.
        """
        st = original_state
        if np.random.random() >= self._failure_rate:
            fail_state_options = State.range(start_state=State.S0, end_state=original_state)
            c = np.random.choice(1, len(fail_state_options))
            st = fail_state_options[c]
        return st

    def failure_rate(self) -> float:
        """
        The rate at which tasks fail.
        :return: The failure rate 0.0 to 1.0
        """
        return self._failure_rate
