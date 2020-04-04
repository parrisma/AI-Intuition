import unittest
from journey11.src.test.srcsink.testsrcsinkgood import TestSrcSinkGood


class TestSrcSink(unittest.TestCase):

    def test_sig_checker_no_errors(self):
        try:
            _ = TestSrcSinkGood()
        except Exception as e:
            self.fail("Unexpected exception [{}]".format(str(e)))
        return


if __name__ == "__main__":
    unittest.main()
