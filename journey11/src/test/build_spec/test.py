import unittest
import logging
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.test.build_spec import BuildSpec


class TestBuildSpec(unittest.TestCase):
    _id = 1

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestBuildSpec._id))
        TestBuildSpec._id += 1
        return

    def test_basics(self):
        # BuildSpec is bootstrapped in the module __init__.py
        current_spec = BuildSpec.get_spec()
        branch = BuildSpec.branch()
        pubsub_settings_yaml = BuildSpec.pubsub_settings_yaml()
        self.assertEqual(BuildSpec.DEFAULT, current_spec)
        self.assertTrue(len(branch) > 0)
        self.assertTrue(len(pubsub_settings_yaml) > 0)
        return


if __name__ == "__main__":
    unittest.main()
