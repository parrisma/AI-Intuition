class Message1:
    _field1: str
    _field2: int

    def __init__(self, **kwargs):
        self._field1 = kwargs.get('field1', str())
        self._field2 = kwargs.get('field2', int())

    @property
    def field(self) -> str:
        return self._field1

    def __str__(self):
        return "Message1:(field1: {} field2:{}".format(self._field1, self._field2)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._field1 == other._field1 and self._field2 == other._field2
        else:
            return False
