from abc import ABC
from enum import Enum, unique


@unique
class CaseProperty(Enum):
    """
    Types of Test Case Property.
    """
    NUM_COMPUTE = 0,
    NUM_TASK = 1,
    NUM_RUN_DAYS = 2
