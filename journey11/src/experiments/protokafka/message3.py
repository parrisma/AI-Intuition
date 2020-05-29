from typing import List
from journey11.src.experiments.protokafka.state import State
from journey11.src.experiments.protokafka.task import Task


class Message3:
    _field_Y: str
    _m3: int
    _state: State
    _tasks: List[Task]

    def __init__(self, **kwargs):
        self._field_Y = kwargs.get('field_Y', str())
        self._m3 = kwargs.get('m3', int())
        self._state = kwargs.get('state', State.S1)
        self._tasks = kwargs.get('tasks', list())

    @property
    def field(self) -> str:
        return self._field_Y

    def __str__(self):
        return "Message1:(field: {} m3:{} state:{} tasks:{})".format(self._field_Y, self._m3, self._state,
                                                                     str(self._tasks))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._field_Y == other._field_Y and self._state == other._state and self._tasks == other._tasks and self._m3 == other._m3
        else:
            return False
