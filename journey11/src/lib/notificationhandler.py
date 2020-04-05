from typing import Callable, Type
import logging
import threading
from journey11.src.lib.reflection import Reflection


class NotificationHandler:
    _MSG_TYPE = 0
    _MSG_HANDLER = 1

    def __init__(self,
                 object_to_be_handler_for,
                 throw_unhandled: bool = False):
        Reflection.check_property_exists(object_to_be_handler_for, "name", str)
        self._object_to_handle = object_to_be_handler_for

        self._handler_dict = dict()
        self._handle_dict_lock = threading.Lock()

        self._throw_unhandled = throw_unhandled
        return

    def register_handler(self,
                         handler_for_message: Callable,
                         message_type: Type):
        if not callable(handler_for_message):
            raise ValueError("Handler for message must be callable")
        with self._handle_dict_lock:
            self._handler_dict[message_type.__name__] = [message_type, handler_for_message]
        return

    def call_handler(self, arg1) -> None:
        """
        Invoke the required call for the object being managed.
        :param arg1: closure object to pass to handler method
        """
        msg_type_name = self.supported_message_type(arg1)
        if msg_type_name is not None:
            logging.info("{} Rx Message Type {}".format(self._object_to_handle.name, str(arg1)))
            ((self._handler_dict[msg_type_name])[NotificationHandler._MSG_HANDLER])(arg1)
        else:
            if self._throw_unhandled:
                msg = "Un-handled message type {}".format(msg_type_name)
                logging.critical(msg)
                raise NotImplementedError(msg)
            else:
                msg = "Un-handled message type {} skipped with no processing".format(msg_type_name)
                logging.warning(msg)
        return

    def supported_message_type(self, message) -> str:
        """
        Return the type name of the supported message (handler dict key) if the message is supported of if the
        message is an instance of a supported message.
        :param message: The type of message being checked as supported.
        :return: The support message type as string
        """
        with self._handle_dict_lock:
            to_add = list()
            msg_type_name = type(message).__name__
            res = None
            if msg_type_name not in self._handler_dict:
                for item in self._handler_dict.values():
                    vt, vc = item
                    if isinstance(message, vt):
                        to_add = [msg_type_name, type(message), vc]
                        res = msg_type_name
                        break
                if res is not None:
                    tn, mt, vc = to_add
                    self._handler_dict[tn] = [mt, vc]
            else:
                res = msg_type_name
        return res
