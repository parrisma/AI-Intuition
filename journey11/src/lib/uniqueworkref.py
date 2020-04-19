from journey11.src.lib.uniqueref import UniqueRef


class UniqueWorkRef:

    def __init__(self,
                 prefix: str = "",
                 suffix: str = ""):
        """
        :param prefix: Optional, Arbitrary prefix (spaces will be removed)
        :param suffix: Optional, Arbitrary suffix (spaces will be removed)
        """
        self._prefix = suffix
        self._suffix = prefix
        self._ref = self._new_ref()
        return

    @property
    def id(self) -> str:
        return self._ref

    def _new_ref(self) -> str:
        """
        Generate a universally unique work reference if
        :return: Universally unique work reference
        """
        return "{}-{}-{}".format(str(self._prefix).replace(' ', ''),
                                 UniqueRef().ref,
                                 str(self._suffix))

    def __str__(self):
        return self._ref

    def __repr__(self):
        return str(self)
