from abc import ABC, abstractmethod
from typing import List
from interface.task import Task
from lib.simpletask import SimpleTask
from lib.state import State
from lib.stateeffortmap import StateEffortMap


class SimpleScenario(ABC):

    def __init__(self,
                 effort_map: StateEffortMap):
        self._num_tasks = 10
        self._effort_map = effort_map
        self._tasks = None
        pass

    @abstractmethod
    def tasks(self) -> List[Task]:
        """
        Return the tasks defined for this scenario.
        :return: a scenario
        """
        if self._tasks is None:
            SimpleTask.process_start_state(State.S0)
            SimpleTask.process_end_state(State.S6)
            self._tasks = list()
            for _ in range(1, self._num_tasks):
                t = SimpleTask(self._effort_map)
                self._tasks.append(t)
        return self._tasks

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the Scenario to it's initial state
        """
        return
