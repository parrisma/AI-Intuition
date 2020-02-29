import uuid
from datetime import datetime
from AIIntuition.journeys.journey5.event import Event, FailureEvent


class Log:
    _file_handle = None
    _file_handle_feature = None
    _fhs = [_file_handle, _file_handle_feature]
    _inst = None

    def __init__(self):
        if Log._inst is None:
            Log._inst = 0
        Log._inst += 1

    def __del__(self):
        Log._inst -= 1
        if Log._inst <= 0:
            for fh in Log._fhs:
                fh.flush()
                fh.close()
                fh = None
            Log._inst = None

    @classmethod
    def log_event(cls,
                  event: Event,
                  *argv) -> None:
        """
        Post a standard form log message to the current sink of the Log Class
        :param event: The event type
        :param argv: The components of the message body - all must support conversion to string
        """
        log_msg = cls.log_message(event, False, *argv)
        print(log_msg)
        cls._log_to_file(log_msg)
        log_msg_f = cls.log_message(event, True, *argv)
        cls._log_to_feature_file(log_msg_f)

    @classmethod
    def log_message(cls,
                    event: Event,
                    as_features: bool,
                    *argv) -> str:
        """
        Return a standard form log message
        :param event: The event type
        :param as_features: Create the log entry 'feature style' for use by AI/ML routines
        :param argv: The components of the message body - all must support conversion to string
        :return: Standard form Log message - current time stamp, event type & message body
        """
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        log_message = ''.join((ts, Event.separator() + ' ', event.as_str(as_features)))
        for arg in argv:
            log_message = ''.join((log_message, str(arg)))

        log_message = log_message.rstrip()
        if log_message[-1] == Event.separator():
            log_message = log_message[0:-1]

        return log_message

    @classmethod
    def _log_file_name(cls) -> str:
        return datetime.now().strftime('%Y-%m-%d-%H-%M-%S-') + uuid.uuid4().hex + '.log'

    @classmethod
    def _log_to_file(cls, log_msg: str) -> None:
        if cls._file_handle is None:
            cls._file_handle = open(cls._log_file_name(), "w")
        cls._file_handle.write(log_msg + '\n')
        return

    @classmethod
    def _feature_file_name(cls) -> str:
        return datetime.now().strftime('%Y-%m-%d-%H-%M-%S-') + uuid.uuid4().hex + '_features.log'

    @classmethod
    def _log_to_feature_file(cls, log_msg: str) -> None:
        if cls._file_handle_feature is None:
            cls._file_handle_feature = open(cls._feature_file_name(), "w")
        cls._file_handle_feature.write(log_msg + '\n')
        return


if __name__ == "__main__":
    ve = ValueError()
    Log.log_event(FailureEvent(), 'Hello', 3142, 'World')
