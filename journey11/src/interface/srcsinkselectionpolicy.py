from abc import ABC, abstractmethod
from typing import Iterable
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.purevirtual import purevirtual


class SrsSinkSelectionPolicy(ABC):
    """
    Policy to select a subset of SrcSinks that best match a given situation
    """

    @abstractmethod
    @purevirtual
    def best_match(self) -> Iterable[SrcSink]:
        """
        The collection of SrcSinks that best match the policy
        :return: SrcSinks that best match the policy
        """
        pass
