from typing import List
from enum import Enum, unique
from copy import deepcopy


@unique
class CPUType(Enum):
    GPU = 'GPU'
    GENERAL = 'CPU'
    BATCH = 'BAT'

    def __str__(self):
        return self.value

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.value + other.value
        else:
            ValueError('Cannot add :' + self.__class__.__name__ + 'with :' + other.__class__.__name__)

    @classmethod
    def cpu_types(cls) -> List['CPUType']:
        return deepcopy([cls.GPU,
                         cls.GENERAL,
                         cls.BATCH
                         ]
                        )
