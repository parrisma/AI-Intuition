import logging


class LoggingSetup:
    _done = False

    def __init__(self):
        if not LoggingSetup._done:
            LoggingSetup._done = True
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        return
