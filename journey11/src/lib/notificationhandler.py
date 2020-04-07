from typing import Callable, Type, Dict
import logging
import threading
from journey11.src.lib.reflection import Reflection
from journey11.src.lib.uniqueref import UniqueRef


class NotificationHandler:
    _MSG_TYPE = 0
    _MSG_HANDLER = 1

    class ActivityNotification:
        """Class to handle timer based activity inside the Handler.
        These timer based activities are added by external party.
        """

        def __init__(self,
                     name: str,
                     interval: float,
                     func: Callable,
                     activity_handler: Callable,
                     stop: bool):
            self._name = name
            self._interval = interval
            self._func = func
            self._activity_handler = activity_handler
            self._stop = stop
            return

        def run(self) -> None:
            self._activity_handler()
            self.go()

        def __call__(self, *args, **kwargs):
            self._func(self)

        def go(self):
            if not self._stop:
                t = threading.Timer(self._interval, self)
                t.daemon = True  # Thread will exit when main program exits.
                t.start()
            else:
                logging.info("Activity {} stopped on request".format(self._name))
            return

        def __str__(self):
            return "ActivityNotification: {}".format(self._name)

        def __repr__(self):
            return self.__str__()

    def __init__(self,
                 object_to_be_handler_for,
                 throw_unhandled: bool = False):
        Reflection.check_property_exists(object_to_be_handler_for, "name", str)
        self._object_to_handle = object_to_be_handler_for

        self._handler_dict = dict()
        self._handle_dict_lock = threading.Lock()

        self._throw_unhandled = throw_unhandled

        self._stop_all_activity = False

        return

    def register_handler(self,
                         handler_for_message: Callable,
                         message_type: Type) -> None:
        """
        Register the given function against the message type - such that when messages of that type arrive
        the given handler is called and passed messages of that type
        :param handler_for_message: Callable handler.
        :param message_type: The Type of message to register the handler against
        """
        if not callable(handler_for_message):
            raise ValueError("Handler for message must be callable")
        with self._handle_dict_lock:
            msg_type_name = message_type.__name__
            if not self.__handler_registered_for_type(message_type):
                self._handler_dict[message_type.__name__] = [message_type, handler_for_message]
            else:
                msg = "Cannot register multiple handlers for a given type [{}]".format(msg_type_name)
                logging.critical(msg)
                raise ValueError(msg)
        return

    def __handler_registered_for_type(self, type_to_check: Type):
        """
        Check if a handler is already registered for the given type
        :param type_to_check: The type to see if there is a handler for.
        :return: True if handler is registered for that type.
        """
        type_name = type_to_check.__name__
        return type_name in self._handler_dict

    def register_activity(self,
                          handler_for_activity: Callable,
                          activity_interval: float,
                          activity_name: str = None) -> None:
        """
        Create a self re-setting timer that sends a message to the Handler such that the given callback is
        invoked at the given interval.
        Activity events are injected into the main handler function so that there is a single stream of events
        for the handler to manage.
        :param handler_for_activity: Callable handler for the timer event
        :param activity_interval: the timer interval
        :param activity_name: (optional) name for the activity.
        :return:
        """
        if not callable(handler_for_activity):
            raise ValueError("Handler for message must be callable")
        if not activity_interval > float(0):
            raise ValueError("timer must be greater than zero - {} was passed".format(activity_interval))
        if activity_name is None:
            activity_name = UniqueRef().ref

        if not self.__handler_registered_for_type(self.ActivityNotification):
            self.register_handler(self.do_activity, self.ActivityNotification)

        self._stop_all_activity = False
        self.ActivityNotification(name=activity_name,
                                  interval=activity_interval,
                                  func=self.call_handler,
                                  activity_handler=handler_for_activity,
                                  stop=self._stop_all_activity).go()

        return

    def stop_all_activity(self) -> None:
        """ Stop all activity by setting the stop flag
        This will cause all activity to not reset the *next* time it fires after the flag is
        set. The activity cannot be restarted it has ot be re registered.
        """
        self._stop_all_activity = True

    @staticmethod
    def do_activity(activity: 'NotificationHandler.ActivityNotification') -> None:
        """
        Call the run method on the given activity - in response to a Timer expiring requiring the activity to
        be executed
        :param activity: The activity to be run.
        """
        logging.info("Activity {} invoked".format(str(activity)))
        activity.run()
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
