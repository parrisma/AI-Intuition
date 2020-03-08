from typing import List

from interface.actor import Actor
from lib.state import State
from lib.simpletask import SimpleTask
from lib.simpleactor import SimpleActor
from interface.scenario import Scenario
from lib.variablecapacity import VariableCapacity
from lib.stateeffortmap import StateEffortMap


class SimpleScenario(Scenario):

    def __init__(self,
                 num_tasks: int,
                 effort_map: StateEffortMap):
        self._a1 = None
        self._a2 = None
        self._a3 = None
        self._a4 = None
        self._a5 = None
        self._a6 = None
        self._actors = None
        self._tasks = None
        self._num_tasks = num_tasks
        self._effort_map = effort_map
        self._team = None

        self._create_actors()
        self._create_tasks()
        self._create_team()

    def get(self) -> List[List[Actor]]:
        """
        A reference to a scenario that can be passed to a simulator
        :return: a scenario
        """
        return self._team

    def reset(self) -> None:
        """
        Reset the Scenario to it's initial state
        """
        if self._actors is not None:
            for a in self._actors:
                a.reset()

        if self._tasks is not None:
            for t in self._tasks:
                t.reset()

        self._inject_tasks()

        return

    def _inject_tasks(self) -> None:
        """
        Add the scenario tasks to the in queue of the primary actor in the tea,
        :return:
        """
        primary_actor = self._a1
        for t in self._tasks:
            primary_actor.task_in(t)
        return

    def _create_actors(self) -> None:
        """
        Create the six actors required for this scenario
        :return: List of Actors.
        """

        # Capacity that is variable in range 1 to 10, but biased to high end.
        cap_10 = VariableCapacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                  [0.01, 0.01, 0.02, 0.03, 0.03, 0.05, 0.05, 0.1, 0.5, 0.2])

        # Capacity that is variable in range 1 to 5, but biased to high end.
        cap_5 = VariableCapacity([1, 2, 3, 4, 5],
                                 [.05, 0.05, 0.1, .6, .2])

        self._a1 = SimpleActor("A1", State.S0, State.S1, 0.0, cap_10)
        self._a2 = SimpleActor("A2", State.S1, State.S2, 0.0, cap_10)
        self._a3 = SimpleActor("A3", State.S2, State.S3, 0.0, cap_5)
        self._a4 = SimpleActor("A4", State.S3, State.S4, 0.0, cap_10)
        self._a5 = SimpleActor("A5", State.S4, State.S5, 0.0, cap_10)
        self._a6 = SimpleActor("A6", State.S5, State.S6, 0.0, cap_10)
        self._actors = [self._a1, self._a2, self._a3, self._a4, self._a5, self._a6]
        return

    def _create_team(self) -> None:
        """
        Create the team that process tasks from initial to terminal state
        :return: the team !
        """
        # [a1, a2 ,a3]
        # a1 = Actor Doing the Work at this spot
        # a2 = Next Actor to pass task to when task done
        # a3 = Actor to pass the task to if the task is reported as failed.
        #
        self._team = [[self._a1, self._a2, self._a1],
                      [self._a2, self._a3, self._a1],
                      [self._a3, self._a4, self._a1],
                      [self._a4, self._a5, self._a1],
                      [self._a5, self._a6, self._a1],
                      [self._a6, None, self._a1]
                      ]
        return

    def _create_tasks(self):
        """
        Create a bag of tasks
        :return: a bag of tasks
        """
        SimpleTask.process_start_state(State.S0)
        SimpleTask.process_end_state(State.S6)
        self._tasks = list()
        for _ in range(1, self._num_tasks):
            t = SimpleTask(self._effort_map)
            self._tasks.append(t)
        return
