from typing import List
from journey11.src.test.dcopy.message2 import Message2


class Message3:
    # Annotation needed by Copy to Protbuf as type hints for some conversions
    _field: str
    _single_m2: Message2
    _list_m2: List[Message2]

    def __init__(self, **kwargs):
        # Default missing to None - this means DCopy will have to rely on annotation to create the
        # target object before copying into it.
        self._field = kwargs.get('field', None)
        self._single_m2 = kwargs.get('single_m2', None)
        self._list_m2 = kwargs.get('list_m2', None)
        return

    def __str__(self):
        return "Message1:(field: {} single_m2:{})".format(self._field, str(self._single_m2))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._field == other._field and self._single_m2 == other._single_m2:
                if len(self._list_m2) == len(other._list_m2):
                    for s, o in zip(self._list_m2, other._list_m2):
                        if s != o:
                            return False
            return True
        else:
            return False
