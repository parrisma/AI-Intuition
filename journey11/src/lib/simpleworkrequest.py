from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.workrequest import WorkRequest
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class SimpleWorkRequest(WorkRequest):

    def __init__(self,
                 unique_work_ref: UniqueWorkRef,
                 originator: SrcSink):
        self._work_ref = unique_work_ref
        self._originator = originator
        return

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference of teh work being requested
        :return: The work reference
        """
        return self._work_ref

    @property
    def originator(self) -> SrcSink:
        """
        The origin the work request came from.
        :return: The task pool
        """
        return self._originator

    def __str__(self):
        """
        Render as string
        :return: String rendering of class instance
        """
        return "Work Request {} from SrcSink {}".format(self._work_ref.id, self._originator.name)
