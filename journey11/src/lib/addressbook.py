import operator
import threading
import datetime
from typing import List
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.capability import Capability
from journey11.src.lib.srcsinkwithtimestamp import SrcSinkWithTimeStamp


class AddressBook:
    CAPABILITY_MATCH_EXACT = float(1)

    def __init__(self):
        self._lock = threading.RLock()
        self._src_sinks_with_timestamp = dict()

    def get(self) -> List['SrcSink']:
        """
        The list of srcsinks in the address book
        :return: List of srcsinks
        """
        with self._lock:
            srcsinks = list(x.srcsink for x in self._src_sinks_with_timestamp.values())
        return srcsinks

    def update(self,
               srcsink: 'SrcSink') -> None:
        """
        Update the given src_sink in the collection of registered srcsinks. If src_sink is not in the collection
        add it with a current time stamp.
        :param srcsink: The src_sink to update / add.
        """
        srcsink_name = srcsink.name
        with self._lock:
            if srcsink_name not in self._src_sinks_with_timestamp:
                self._src_sinks_with_timestamp[srcsink_name] = SrcSinkWithTimeStamp(srcsink=srcsink,
                                                                                    time_stamp=datetime.datetime.now())
            else:
                self._src_sinks_with_timestamp[srcsink_name].time_stamp = datetime.datetime.now()
        return

    def _recent(self,
                last_seen: datetime,
                max_age_in_seconds: float) -> bool:
        return float((datetime.datetime.now() - last_seen).seconds) <= max_age_in_seconds

    def get_with_capabilities(self,
                              required_capabilities: List[Capability],
                              match_threshold: float = CAPABILITY_MATCH_EXACT,
                              max_age_in_seconds: float = None) -> SrcSink:
        """
        Get a SrcSin with matching capabilities, and if there are more than one get the one with the newest timestamp.
        :param required_capabilities: The required capabilities
        :param match_threshold: The minimum match level to the required capabilities 0.0 to 1.0 = exact
        :param max_age_in_seconds: (optional) the max age of the SrcSink since the last ping - the get will remove
            any capability matched SrcSinks that are older than this threshold.
        :return:
        """
        if match_threshold > 1.0 or match_threshold < 0:
            raise ValueError("match_threshold must be in range 0.0 to 1.0 :{} was given".format(str(match_threshold)))

        res = None
        to_consider = list()
        for sswt in self._src_sinks_with_timestamp.values():
            ef = Capability.equivalence_factor(given_capabilities=sswt.srcsink.capabilities,
                                               required_capabilities=required_capabilities)
            if ef >= match_threshold:
                if max_age_in_seconds is None:
                    to_consider.append([ef, sswt.time_stamp, sswt])
                else:
                    if self._recent(sswt.time_stamp, max_age_in_seconds):
                        to_consider.append([ef, sswt.time_stamp, sswt])
        if len(to_consider) > 0:
            if len(to_consider) > 1:
                to_consider = sorted(to_consider, key=operator.itemgetter(0, 1))
            res = (to_consider[-1])[2].srcsink
        return res
