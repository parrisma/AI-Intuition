from copy import deepcopy
from journey10.task import Task
from state import State
from journey10.stateeffortmap import StateEffortMap


class SimpleTask(Task):
    _start_state = State.S0
    _terminal_state = State.S9
    _global_id = 0

    def __init__(self,
                 effort_map: StateEffortMap):
        """
        Constructor
        """
        self._state = self._start_state
        self._id = self._global_id
        self._global_id += 1
        self._effort_map = effort_map
        self._remaining_effort = None
        self.state = self._start_state

    @property
    def id(self) -> int:
        """
        The globally unique id of the task
        :return: Globally Unique id of the task
        """
        return deepcopy(self._id)

    @property
    def state(self) -> State:
        """
        Current State of the task.
        :return: Current State
        """
        return deepcopy(self._state)

    @state.setter
    def state(self,
              s: State) -> None:
        """
        Set the tasks new state
        :param s: the state to set the task to
        """
        self._state = deepcopy(s)
        self._remaining_effort = self._effort_map.effort()
        return

    @property
    def start_state(self) -> State:
        """
        The defined start (reset) state of the Task
        :return: The Start State
        """
        return State.S0

    @property
    def terminal_state(self) -> State:
        """
        The defined terminal (end) state of the Task - i.e. when teh task is done
        :return: The Terminal (end) state of the task
        """
        return State.S9

    def do_work(self,
                work: int) -> int:
        """
        Do the given units of work, i.e. decrement the number of work units from the residual effort remaining
        for the task. If the number of work units is greater than the residual then the difference of work
        units is 'lost' as the task will absorb any additional.
        :param work: The number of units of work to do.
        :return: The remaining units of work, where 0 means the task ne
        """
        self._remaining_effort = min(0, self._remaining_effort - work)
        return deepcopy(self._remaining_effort)

    def __str__(self) -> str:
        """
        Render the task as a string
        :return: Task as string
        """
        return "Task id[{0}] in State[{1}]".format(str(self._id), str(self._state))
