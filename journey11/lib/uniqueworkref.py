import uuid


class UniqueWorkRef:

    def __init__(self,
                 task_id: int,
                 pool_name: str):
        self._pool_name = pool_name
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
        return "{}-{}-{}".format(str(self._pool_name).replace(' ', ''),
                                 str(uuid.uuid4()).replace('-', ''),
                                 str(self._task_id))
