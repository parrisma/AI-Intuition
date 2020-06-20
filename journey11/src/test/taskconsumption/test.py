import logging
import unittest
import random
from journey11.src.lib.randomtaskconsumptionpolicy import RandomTaskConsumptionPolicy
from journey11.src.main.simple.simpletaskmetadata import SimpleTaskMetaData
from src.lib.aitrace.trace import Trace


class TestTaskConsumptionRate(unittest.TestCase):
    _test_task_meta = SimpleTaskMetaData(1)

    @classmethod
    def setUp(cls) -> None:
        Trace()

    def test_boundaries(self):
        """
        Test boundary cases.
        """
        # Should raise
        self.assertRaises(ValueError, RandomTaskConsumptionPolicy, -1.0)
        self.assertRaises(ValueError, RandomTaskConsumptionPolicy, 1.01)

        # Should not raise
        self.assertEqual(False, RandomTaskConsumptionPolicy(0.0).process_task(self._test_task_meta))
        self.assertEqual(True, RandomTaskConsumptionPolicy(1.0).process_task(self._test_task_meta))

    def test_center(self):
        """
        Test center state, we pick a random target processing rate and then check that the true cases
        converge on that target to a small margin of error within 10K test cases.
        """

        test_rates = list()
        for _ in range(10):
            test_rates.append(round(random.random(), 3))
        test_rates.append(float(0.0))
        test_rates.append(float(0.5))
        test_rates.append(float(1.0))

        for target_rate in test_rates:
            rtcp = RandomTaskConsumptionPolicy(target_rate)

            num_tests = 10000
            true_count = 0
            for _ in range(num_tests):
                if rtcp.process_task(self._test_task_meta):
                    true_count += 1

            err = 0.01 - (target_rate - (true_count / num_tests))
            logging.info(str(err))
            self.assertAlmostEqual(float(0), err, places=1)
        return


if __name__ == '__main__':
    unittest.main()
