from journey11.src.test.dcopy.l3 import L3


class L2:
    # Annotation needed by Copy to Protbuf as type hints for some conversions
    _single_l3: L3
    _s2: str

    def __init__(self, **kwargs):
        # Default missing to None - this means DCopy will have to rely on annotation to create the
        # target object before copying into it.
        self._single_l3 = kwargs.get('single_l3', None)
        self._s2 = kwargs.get('s2', None)
        return

    def __str__(self):
        return "L2 :(field: {} single_l3:{})".format(self._s2, str(self._single_l3))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._s2 == other._s2 and self._single_l3 == other._single_l3:
                return True
        else:
            return False
