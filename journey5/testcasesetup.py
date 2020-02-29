from typing import Tuple
from collections.abc import Iterable
from enum import Enum
from AIIntuition.journeys.journey5.policy import Policy
from AIIntuition.journeys.journey5.cases import Cases
from AIIntuition.journeys.journey5.randomcase import RandomCase


class TestCaseSetUp:
    """
    In the test we create a single data center
    created randomly and if applicable according to the defined probability distributions of the type
    """

    class TestCase(Enum):
        COMPUTE_RESTRICTED = Cases.ComputeRestricted
        MEMORY_RESTRICTED = Cases.MemoryRestricted
        MULTI_DATACENTER = Cases.MultiDataCenterRestricted
        CORE_MISMATCH = Cases.CoreDemandActualMistMatch
        RANDOM = RandomCase

    @classmethod
    def set_up(cls,
               test_case: 'TestCaseSetUp.TestCase') -> Tuple[int, int, Policy, Iterable, int]:
        """
        Set-up the environment for a schedule test case.
            Note: The DataCenters, Hosts & Apps are available to the caller via the Class methods on these Types
            that return lists of all objects of the given type.
        :return:
            The number of hosts created
            The number of applications created
            The Host Selection Policy used by the scheduler
            The Host iterator used by the scheduler
            The number of 24 hour periods to run the schedule simulation for
        """

        return test_case.value()
