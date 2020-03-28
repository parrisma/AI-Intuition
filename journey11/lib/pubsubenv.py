import logging
from pubsub import pub


class PubSubEnv:
    _singleton_init = False

    class PubSubEnvExceptionHandler(pub.IListenerExcHandler):
        def __call__(self, listener_id, topic_obj):
            logging.info("Listener Id [{}] raised an exception".format(listener_id))
            return

    def __init__(self):
        # Register PubSubEnv exception handler.
        if not self._singleton_init:
            self._singleton_init = True
            pub.setListenerExcHandler(PubSubEnv.PubSubEnvExceptionHandler())
