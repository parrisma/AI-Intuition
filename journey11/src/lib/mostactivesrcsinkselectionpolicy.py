import operator
from typing import Iterable, List
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.srcsinkmetadata import SrcSinkMetaData
from journey11.src.interface.srcsinkselectionpolicy import SrsSinkSelectionPolicy


class MostActiveSrcSinkSelectionPolicy(SrsSinkSelectionPolicy):
    """
    Select the SrcSinks that are the most active and thus the most appropriate to share addresses of in
    response to a pin request
    """

    def __init__(self,
                 max_to_match: int,
                 srcsinks_meta: List[SrcSinkMetaData]):
        """
        :param max_to_match: The maximum number of SrcSinks to return in best match call.
        :param srcsinks_meta: The list of SrcSinks to apply the policy to.
        """
        if max_to_match <= 1:
            raise ValueError("Match to match must be >= to 1 : {} was given".format(str(max_to_match)))
        self._max_to_match = max_to_match
        self._srcsinks_meta = srcsinks_meta
        return

    def best_match(self) -> Iterable[SrcSink]:
        """
        The collection of SrcSinks that best match the policy
        :return: SrcSinks that best match the policy
        """
        sorted_srcsink_meta = sorted(self._srcsinks_meta, key=operator.attrgetter('last_ping'))
        return [x.srcsink for x in sorted_srcsink_meta[(-min(len(sorted_srcsink_meta), self._max_to_match)):]]
