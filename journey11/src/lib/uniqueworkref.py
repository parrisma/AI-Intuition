from journey11.src.lib.uniqueref import UniqueRef


class UniqueWorkRef:
    # Annotation
    _ref: str

    def __init__(self, **kwargs):
        """
        :param prefix: Optional, Arbitrary prefix (spaces will be removed)
        :param suffix: Optional, Arbitrary suffix (spaces will be removed)
        """
        _prefix = kwargs.get('prefix', str())
        _suffix = kwargs.get('suffix', str())
        if _prefix is None:
            _prefix = str()
        else:
            _prefix = _prefix.replace(' ', '')
        if _suffix is None:
            _suffix = str()
        else:
            _suffix = _suffix.replace(' ', '')

        self._ref = UniqueWorkRef._new_ref(prefix=_prefix, suffix=_suffix)
        return

    @property
    def id(self) -> str:
        return self._ref

    @staticmethod
    def _new_ref(prefix: str, suffix: str) -> str:
        """
        Generate a universally unique work reference if
        :return: Universally unique work reference
        """
        return "{}-{}-{}".format(str(prefix),
                                 UniqueRef().ref,
                                 str(suffix))

    def __str__(self):
        return self._ref

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._ref == other._ref
        else:
            return False
