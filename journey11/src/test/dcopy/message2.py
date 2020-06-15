from typing import List


class Message2:
    # Annotation needed by Copy to Protbuf as type hints for some conversions
    _field: str
    _strings: List[str]
    _double: float
    _float: float
    _int32: int
    _int64: int
    _bool: bool
    _bytes: bytes

    def __init__(self, **kwargs):
        # Default missing to None - this means DCopy will have to rely on annotation to create the
        # target object before copying into it.
        self._field = kwargs.get('field', None)
        self._strings = kwargs.get('strings', None)
        self._double = kwargs.get('_double', None)
        self._float = kwargs.get('_float', None)
        self._int32 = kwargs.get('_int32', None)
        self._int64 = kwargs.get('_int64', None)
        self._bool = kwargs.get('_bool', None)
        self._bytes = kwargs.get('_bytes', None)
        return

    def __str__(self):
        return "Message1:(field: {} strings:{})".format(self._field, str(self._strings))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._field == other._field and self._double == other._double and \
                    self._float == other._float and self._int32 == other._int32 and self._int64 == other._int64 and \
                    self._bool == other._bool and self._bytes == other._bytes:
                if len(self._strings) == len(other._strings):
                    for s, o in zip(self._strings, other._strings):
                        if s != o:
                            return False
            return True
        else:
            return False
