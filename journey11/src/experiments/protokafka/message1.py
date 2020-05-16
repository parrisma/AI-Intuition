from typing import List
from journey11.src.experiments.protokafka.state import State
from journey11.src.experiments.protokafka.task import Task


class Message1:
    _field: str
    _state: State
    _tasks: List[Task]

    def __init__(self, **kwargs):
        self._field = kwargs.get('field', str())
        self._state = kwargs.get('state', State.S1)
        self._tasks = kwargs.get('tasks', list())

    @property
    def field(self) -> str:
        return self._field

    def __str__(self):
        return "Message1:(field: {} state:{}, tasks:{})".format(self._field, self._state, str(self._tasks))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._field == other._field and self._state == other._state and self._tasks == other._tasks
        else:
            return False
