from typing import Callable, Type
import logging
from journey11.src.lib.reflection import Reflection
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotification import WorkNotification


class NotificationHandler:
    def __init__(self,
                 object_to_be_handler_for):
        Reflection.check_property_exists(object_to_be_handler_for, "name", str)
        Reflection.check_property_exists(object_to_be_handler_for, "topic", str)
        Reflection.check_method_exists(object_to_be_handler_for, "_do_notification", [TaskNotification])
        Reflection.check_method_exists(object_to_be_handler_for, "_do_work", [WorkNotification])
        self._object_to_handle = object_to_be_handler_for

        self._handler_dict = dict()
        return

    def register_handler(self,
                         handler_for_message: Callable,
                         message_type: Type):
        if not callable(handler_for_message):
            raise ValueError("Handler for message must be callable")
        self._handler_dict[message_type.__name__] = [message_type, handler_for_message]
        return

    def call_handler(self, arg1) -> None:
        """
        Invoke the required call for the object being managed.
        :param arg1: closure object to pass to handler method
        """
        arg_type_name = type(arg1).__name__
        if arg_type_name in self._handler_dict:

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
