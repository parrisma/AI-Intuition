from abc import ABC, abstractmethod
from typing import List
from journey11.src.lib.purevirtual import purevirtual


class TaskGenerationPolicy(ABC):
    @abstractmethod
    @purevirtual
    def num_to_generate(self) -> List[int]:
        """
        A list of task efforts for the tasks to be created
        :return: A List of task efforts
        """
        pass
