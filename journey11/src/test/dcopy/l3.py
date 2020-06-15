from journey11.src.test.dcopy.l4 import L4


class L3:
    # Annotation needed by Copy to Protbuf as type hints for some conversions
    _single_l4: L4
    _s3: str

    def __init__(self, **kwargs):
        # Default missing to None - this means DCopy will have to rely on annotation to create the
        # target object before copying into it.
        self._single_l4 = kwargs.get('single_l4', None)
        self._s3 = kwargs.get('s3', None)
        return

    def __str__(self):
        return "L3 :(field: {} single_l4:{})".format(self._s3, str(self._single_l4))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._s3 == other._s3 and self._single_l4 == other._single_l4:
                return True
        else:
            return False
