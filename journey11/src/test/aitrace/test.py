import unittest
import logging
from src.lib.aitrace.trace import Trace
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.test.gibberish.gibberish import Gibberish


class TestAITrace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        return

    def test_simple(self):
        try:
            Trace()
            Trace.log().debug("XX")
        except Exception as e:
            print(str(e))
        return


if __name__ == "__main__":
    unittest.main()
