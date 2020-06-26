import unittest
from journey11.src.lib.envboot.envbootstrap import EnvBootstrap
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.test.gibberish.gibberish import Gibberish


class TestAITrace(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        EnvBootstrap()
        return

    def test_simple(self):
        try:
            for i in range(100):
                Trace.log().debug("XX-{}".format(i))
        except Exception as e:
            print(str(e))
        return


if __name__ == "__main__":
    unittest.main()
