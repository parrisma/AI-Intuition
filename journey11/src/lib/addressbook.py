import operator
import threading
import datetime
from typing import List
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.capability import Capability
from journey11.src.lib.srcsinkwithtimestamp import SrcSinkWithTimeStamp


class AddressBook:

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
                              capabilities: List[Capability],
                              max_age_in_seconds: float = None) -> SrcSink:
        """
        Get a SrcSin with matching capabilities, and if there are more than one get the one with the newest timestamp.
        :param capabilities: The required capabilities
        :param max_age_in_seconds: (optional) the max age of the SrcSink since the last ping - the get will remove
            any capability matched SrcSinks that are older than this threshold.
        :return:
        """
        res = None
        to_consider = list()
        for sswt in self._src_sinks_with_timestamp.values():
            if Capability.equivalence_factor(sswt.srcsink.capabilities, capabilities) == float(1):
                if max_age_in_seconds is None:
                    to_consider.append(sswt)
                else:
                    if self._recent(sswt.time_stamp, max_age_in_seconds):
                        to_consider.append(sswt)
        if len(to_consider) > 0:
            if len(to_consider) > 1:
                to_consider = sorted(to_consider, key=operator.attrgetter('time_stamp'))
            res = to_consider[-1].srcsink
        return res
