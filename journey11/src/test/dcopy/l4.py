from journey11.src.test.dcopy.message2 import Message2


class L4:
    # Annotation needed by Copy to Protbuf as type hints for some conversions
    _single_m2: Message2
    _s4: str

    def __init__(self, **kwargs):
        # Default missing to None - this means DCopy will have to rely on annotation to create the
        # target object before copying into it.
        self._single_m2 = kwargs.get('single_m2', None)
        self._s4 = kwargs.get('s4', None)
        return

    def __str__(self):
        return "L4 :(field: {} single_m2:{})".format(self._s4, str(self._single_m2))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._s4 == other._s4 and self._single_m2 == other._single_m2:
                return True
        else:
            return False
