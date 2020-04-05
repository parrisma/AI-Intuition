import uuid


class UniqueWorkRef:

    def __init__(self,
                 task_id: str,
                 originator_id: str):
        self._originator_id = originator_id
        self._task_id = task_id
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
        return "{}-{}-{}".format(str(self._originator_id).replace(' ', ''),
                                 str(uuid.uuid4()).replace('-', ''),
                                 str(self._task_id))

    def __str__(self):
        return self._ref

    def __repr__(self):
        return str(self)
