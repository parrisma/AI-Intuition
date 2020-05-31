class Message2:
    _field3: str
    _field4: float

    def __init__(self, **kwargs):
        self._field3 = kwargs.get('field3', str())
        self._field4 = kwargs.get('field4', float())

    @property
    def field(self) -> str:
        return self._field3

    def __str__(self):
        return "Message1:(field3: {} field4:{}".format(self._field3, self._field4)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._field3 == other._field3 and self._field4 == other._field4
        else:
            return False
