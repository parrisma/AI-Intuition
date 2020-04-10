import datetime
from journey11.src.interface.srcsink import SrcSink


class SrcSinkWithTimeStamp:
    def __init__(self,
                 time_stamp: datetime,
                 sender_srcsink: SrcSink):
        self._time_stamp = time_stamp
        self._sender_src_sink = sender_srcsink
        return

    @property
    def sender_srcsink(self) -> SrcSink:
        return self._sender_src_sink

    @property
    def time_stamp(self) -> datetime:
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self,
                   t: datetime) -> None:
        self._time_stamp = t
        return
