from journey5.compute import Compute
from journey5.host import Host
from journey5.OutOfMemoryException import OutOfMemoryException
from journey5.FailedToCompleteException import FailedToCompleteException
from journey5.log import Log
from journey5.event import SchedulerEvent, HostEvent, TaskEvent, FailureEvent
from journey5.case import Case
from journey5.testcasesetup import TestCaseSetUp


class Scheduler:

    def __init__(self,
                 test_case: Case):
        """
        Instantiate a chosen schedule test case that sets up a schedule environment
        """
        self._num_hosts = None
        self._num_apps = None
        self._policy = None
        self._compute_iter = None

        self._num_hosts, self._num_apps, self._policy, self._compute_iter, self._num_run_days = \
            test_case.set_up()

    def run(self) -> None:
        """
        Run the test case given
        """
        Log.log_event(SchedulerEvent(SchedulerEvent.SchedulerEventType.START))

        for day in range(0, self._num_run_days):
            Log.log_event(SchedulerEvent(SchedulerEvent.SchedulerEventType.NEW_DAY), str(day + 1))
            for gmt_hour_of_day in range(0, 23):
                for c in range(0, self._num_hosts):
                    hst = self.next_compute()
                    for i in range(0, hst.num_associated_task):
                        try:
                            hst.run_next_task(gmt_hour_of_day)
                        except (OutOfMemoryException, FailedToCompleteException) as e:
                            Log.log_event(FailureEvent(exception=e, compute=e.compute, task=e.task_meta_data))
                            self._policy.select_optimal_compute(e.task_meta_data).associate_task(e.task_meta_data)  # re schedule
            for h in Host.all_hosts():
                Log.log_event(HostEvent(HostEvent.HostEventType.STATUS, h))
                for t in h.all_tasks():
                    Log.log_event(TaskEvent(TaskEvent.TaskEventType.STATUS, t))
        Log.log_event(SchedulerEvent(SchedulerEvent.SchedulerEventType.COMPLETE),
                      "Scheduler done after allotted run time ")
        return

    def next_compute(self) -> Compute:
        """
        Random iteration over all existing compute resources, once all resources have been iterated over
        the random iteration is reset and starts again.
        :return: Compute resource from random (& infinite) iteration.
        """
        return next(self._compute_iter)


if __name__ == "__main__":
    Scheduler(TestCaseSetUp.TestCase.CORE_MISMATCH.value).run()
