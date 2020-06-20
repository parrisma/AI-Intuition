import unittest
from src.lib.aitrace.trace import Trace
from journey11.src.test.srcsink.testsrcsink import TestSrcSink


class TestSrcSink(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Trace()

    def test_sig_checker_no_errors(self):
        try:
            _ = TestSrcSink()
        except Exception as e:
            self.fail("Unexpected exception [{}]".format(str(e)))
        return


if __name__ == "__main__":
    unittest.main()
