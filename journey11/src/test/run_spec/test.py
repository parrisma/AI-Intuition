import unittest
import logging
from src.lib.aitrace.trace import Trace
from journey11.src.test.run_spec import RunSpec


class TestBuildSpec(unittest.TestCase):
    _id = 1

    @classmethod
    def setUpClass(cls):
        Trace()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestBuildSpec._id))
        TestBuildSpec._id += 1
        return

    def test_basics(self):
        # BuildSpec is bootstrapped in the module __init__.py
        current_spec = RunSpec.get_spec()
        branch = RunSpec.branch()
        pubsub_settings_yaml = RunSpec.pubsub_settings_yaml()
        self.assertEqual(RunSpec.DEFAULT, current_spec)
        self.assertTrue(len(branch) > 0)
        self.assertTrue(len(pubsub_settings_yaml) > 0)
        return


if __name__ == "__main__":
    unittest.main()
