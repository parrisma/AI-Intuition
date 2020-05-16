from typing import List
from journey11.src.test.dcopy.state import State
from journey11.src.test.dcopy.task import Task


class Message1:
    _field: str
    _state: State
    _tasks: List[Task]
    _strings: List[str]

    def __init__(self, **kwargs):
        self._field = kwargs.get('field', str())
        self._state = kwargs.get('state', State.S1)
        self._tasks = kwargs.get('tasks', list())
        self._strings = kwargs.get('strings', list())

    def __str__(self):
        return "Message1:(field: {} state:{}, tasks:{} strings:{})".format(self._field, self._state, str(self._tasks),
                                                                           str(self._strings))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._field == other._field and self._state == other._state:
                if len(self._tasks) == len(other._tasks):
                    for s, o in zip(self._tasks, other._tasks):
                        if s != o:
                            return False
            if len(self._strings) == len(other._strings):
                for s, o in zip(self._strings, other._strings):
                    if s != o:
                        return False
            return True
        else:
            return False
