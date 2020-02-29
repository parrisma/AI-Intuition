from journey5.scheduler import Scheduler
from journey5.testcasesetup import TestCaseSetUp
from journey5.event import Event

if __name__ == "__main__":
    Scheduler(TestCaseSetUp.TestCase.RANDOM.value).run()
    # Scheduler(TestCaseSetUp.TestCase.CORE_MISMATCH.value).run()
    # Scheduler(TestCaseSetUp.TestCase.MEMORY_RESTRICTED.value).run()
    Event.dump_feature_maps()
