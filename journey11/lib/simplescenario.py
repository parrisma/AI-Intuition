from typing import Iterable
from journey10.interface.task import Task
from journey10.lib.simpletask import SimpleTask
from journey10.lib.state import State
from journey10.lib.stateeffortmap import StateEffortMap
from journey11.interface.scenario import Scenario
from journey11.interface.agent import Agent


class SimpleScenario(Scenario):

    def __init__(self,
                 effort_map: StateEffortMap):
        self._num_tasks = 10
        self._effort_map = effort_map
        self._tasks = None
        self._agents = None
        return

    def tasks(self) -> Iterable[Task]:
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

    def agents(self) -> Iterable[Agent]:
        """
        Return the agents that will do work.
        :return: a iterable of agents
        """
        return self._agents

    def reset(self) -> None:
        """
        Reset the Scenario to it's initial state
        """
        return
