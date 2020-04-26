import unittest
import logging
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.main.simple.simpletaskgenerationpolicyoneoffbatchuniform import \
    SimpleTaskGenerationPolicyOneOffBatchUniform


class TestAddressBook(unittest.TestCase):
    _id = 1

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestAddressBook._id))
        self._id += 1
        return

    def tearDown(self) -> None:
        return

    def test_one_off_batch(self):
        batch_size = 97
        effort = 3142
        expected_results = [[batch_size, effort], [0, 0], [0, 0], [0, 0], [0, 0]]
        stgpoob = SimpleTaskGenerationPolicyOneOffBatchUniform(batch_size=batch_size, effort=effort)
        for expected_num, effort in expected_results:
            res = stgpoob.num_to_generate()
            self.assertEqual(expected_num, len(res))
            for eff in res:
                self.assertEqual(effort, eff)
        return


if __name__ == "__main__":
    unittest.main()
