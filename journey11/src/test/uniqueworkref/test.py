import unittest
import random
import re
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.uniquetopic import UniqueTopic


class TestTopic(unittest.TestCase):
    # No Prefix (None) & some random prefixes.
    pref = [None,
            'understand',
            'tricky',
            'telling',
            'receptive',
            'bereave',
            'imprint',
            'tell',
            'seat',
            'toys',
            'abject',
            'silky',
            'milky',
            'disagreeable',
            'violate',
            'frantic',
            'scene',
            'moldy',
            'blossom',
            'church',
            'implore']

    pattern_no_prefix = re.compile("^[A-Za-z0-9]+$")
    pattern_with_prefix = re.compile("^[A-Za-z0-9]+.[A-Za-z0-9]+$")

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def test_no_prefix(self):
        ut = UniqueTopic().topic()
        self.assertTrue(TestTopic.pattern_no_prefix.match(ut))

    def test_with_prefix(self):
        ut = UniqueTopic().topic('pref')
        self.assertTrue(TestTopic.pattern_with_prefix.match(ut))

    def test_unique(self):
        have_seen = dict()
        for _ in range(10000):
            pref = random.choice(TestTopic.pref)
            ut = UniqueTopic().topic(pref)
            if pref is None:
                self.assertTrue(TestTopic.pattern_no_prefix.match(ut))
            else:
                self.assertTrue(TestTopic.pattern_with_prefix.match(ut))
            self.assertFalse(ut in have_seen)
            have_seen[ut] = True


if __name__ == "__main__":
    unittest.main()
