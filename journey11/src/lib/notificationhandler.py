import logging
from journey11.src.lib.reflection import Reflection
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotification import WorkNotification


class NotificationHandler:
    def __init__(self,
                 object_to_be_handler_for):
        Reflection.check_property_exists(object_to_be_handler_for, "name")
        Reflection.check_method_exists(object_to_be_handler_for, "_do_notification")
        Reflection.check_method_exists(object_to_be_handler_for, "_do_work")
        self._object_to_handle = object_to_be_handler_for
        return

    def call_handler(self, arg1) -> None:
        """
        Invoke the required call for the object being managed.
        :param arg1: closure object to pass to handler method
        """
        if isinstance(arg1, TaskNotification):
            logging.info("{} Rx TaskNotification {}".format(self._object_to_handle.name, arg1.work_ref.id))
            self._object_to_handle._do_notification(arg1)
        elif isinstance(arg1, WorkNotification):
            logging.info("{} Rx WorkNotification {}".format(self._object_to_handle.name, arg1.work_ref.id))
            self._object_to_handle._do_work(arg1)
        else:
            msg = "Unexpected type [{}] passed to {}.__call__".format(type(arg1), self.__class__.__name__)
            logging.critical("Unexpected type [{}] passed to {}.__call__".format(type(arg1), self.__class__.__name__))
            raise ValueError(msg)
        return
