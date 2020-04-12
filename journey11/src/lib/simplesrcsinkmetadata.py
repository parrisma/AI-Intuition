from datetime import datetime
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.srcsinkmetadata import SrcSinkMetaData


class SimpleSrcSinkMetaData(SrcSinkMetaData):

    def __init__(self,
                 srcsink_with_timestamp: SrcSink.SrcSinkWithTimeStamp):
        self._src_sink_with_timestamp = srcsink_with_timestamp
        return

    @property
    def last_ping(self) -> datetime:
        """
        The datetime of the last ping from the SrcSink
        :return: Date Time of last SrcSink ping
        """
        return self._src_sink_with_timestamp.time_stamp

    @property
    def srcsink(self) -> SrcSink:
        """
        The SrcSink the Meta data relates to.
        :return: SrcSink.
        """
        return self._src_sink_with_timestamp.srcsink
