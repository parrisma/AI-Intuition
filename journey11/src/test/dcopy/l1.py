from journey11.src.test.dcopy.l2 import L2


class L1:
    # Annotation needed by Copy to Protbuf as type hints for some conversions
    _single_l2: L2
    _s1: str

    def __init__(self, **kwargs):
        # Default missing to None - this means DCopy will have to rely on annotation to create the
        # target object before copying into it.
        self._single_l2 = kwargs.get('single_l2', None)
        self._s1 = kwargs.get('s1', None)
        return

    def __str__(self):
        return "L1 :(field: {} single_l4:{})".format(self._s1, str(self._single_l2))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._s1 == other._s1 and self._single_l2 == other._single_l2:
                return True
        else:
            return False
