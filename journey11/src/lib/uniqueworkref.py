from journey11.src.lib.uniqueref import UniqueRef


class UniqueWorkRef:

    def __init__(self,
                 subject_name: str,
                 work_item_ref: str):
        """
        :param subject_name: The id of the subject (object) of the work reference
        :param work_item_ref: The topic of the originator of the work
        """
        self._originator_id = work_item_ref
        self._subject_id = subject_name
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
                                 UniqueRef().ref,
                                 str(self._subject_id))

    def __str__(self):
        return self._ref

    def __repr__(self):
        return str(self)
