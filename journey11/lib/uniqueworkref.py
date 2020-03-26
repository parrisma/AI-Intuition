import uuid


class UniqueWorkRef:

    def __init__(self):
        self._ref = self._new_ref()

    @property
    def id(self) -> str:
        return self._ref

    @classmethod
    def _new_ref(cls) -> str:
        """
        Generate a universally unique work reference if
        :return: Universally unique work reference
        """
        return str(uuid.uuid4()).replace('-', '')
