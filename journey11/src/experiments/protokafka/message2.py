from typing import List
from journey11.src.experiments.protokafka.state import State
from journey11.src.experiments.protokafka.task import Task


class Message2:
    _field_X: str
    _m2: int
    _state: State
    _tasks: List[Task]

    def __init__(self, **kwargs):
        self._field_X = kwargs.get('field_X', str())
        self._m2 = kwargs.get('m2', int())
        self._state = kwargs.get('state', State.S1)
        self._tasks = kwargs.get('tasks', list())

    @property
    def field(self) -> str:
        return self._field_X

    def __str__(self):
        return "Message1:(field: {} m2: {} state:{}, tasks:{})".format(self._field_X, self._m2, self._state,
                                                                       str(self._tasks))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._field_X == other._field_X and self._state == other._state and self._tasks == other._tasks and self._m2 == other._m2
        else:
            return False
