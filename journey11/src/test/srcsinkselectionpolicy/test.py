import operator
import unittest
import datetime
import logging
import numpy as np
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.mostactivesrcsinkselectionpolicy import MostActiveSrcSinkSelectionPolicy
from journey11.src.lib.srcsinkwithtimestamp import SrcSinkWithTimeStamp
from journey11.src.main.simple.simplesrcsinkmetadata import SimpleSrcSinkMetaData
from journey11.src.test.srcsinkselectionpolicy.dummysrcsink import DummySrcSink


class TestSrcSinkSelectionPolicy(unittest.TestCase):
    _pi_day = datetime.datetime(year=2015, month=3, day=14, hour=9, minute=26, second=53)

    @classmethod
    def setUpClass(cls):
        LoggingSetup()
        logging.info(TestSrcSinkSelectionPolicy._pi_day.strftime("%m.%d%y%H%M%S"))
        return

    def test_top_n_by_last_update(self):
        srcsinks_ts = list()
        num_to_test = 5
        test_set_size = 20
        random_offsets = np.random.choice(test_set_size * 10, size=test_set_size, replace=False)
        for i in range(test_set_size):
            ts = TestSrcSinkSelectionPolicy._pi_day + datetime.timedelta(seconds=int(random_offsets[i]))
            srcsinks_ts.append(SrcSinkWithTimeStamp(time_stamp=ts,
                                                    srcsink=DummySrcSink("DummySrcSink-{}".format(i))))

        # Sort & Grab last num_to_test as 'most recent' for the expected return
        srcsinks_ts = sorted(srcsinks_ts, key=operator.attrgetter('time_stamp'))
        expected = [x.srcsink for x in srcsinks_ts[-num_to_test:]]

        # Convert to Meta to pass to Policy
        srcsinks_meta = [SimpleSrcSinkMetaData(x) for x in srcsinks_ts]

        # Create & prime th Most Active Policy
        masssp = MostActiveSrcSinkSelectionPolicy(max_to_match=num_to_test, srcsinks_meta=srcsinks_meta)
        actual = masssp.best_match()

        self.assertEqual(len(expected), len(actual))
        for e, a in zip(expected, actual):
            self.assertEqual(e.name, a.name)
        return


if __name__ == "__main__":
    unittest.main()
