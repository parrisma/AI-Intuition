import unittest
import random
import re
import kpubsubai
from src.lib.aitrace.trace import Trace
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.test.kpubsub.test import KPuBsubUtil


class TestUniqueRef(unittest.TestCase):
    # No Prefix (None) & some random prefixes.
    pref = [None,
            'confuse', 'save', 'sparkle', 'fear',
            'bawdy', 'coach', 'childlike', 'report',
            'ants', 'different', 'strap', 'narrow',
            'picayune', 'aloof', 'sin', 'end',
            'protect', 'giants', 'cute', 'literate']

    sufx = [None,
            'ill', 'pin', 'quartz', 'shade',
            'argument', 'unaccountable', 'stiff', 'groan',
            'inject', 'cheap', 'grubby', 'idea',
            'sea', 'delight', 'disarm', 'small',
            'develop', 'healthy', 'placid', 'lavish']

    @classmethod
    def setUpClass(cls):
        Trace()

    def test_no_prefix_or_suffix(self):
        pattern_no_prefix_no_suffix = re.compile("^-[A-Za-z0-9]+-$")

        ut = UniqueWorkRef().id
        self.assertTrue(pattern_no_prefix_no_suffix.match(ut))

        ut = UniqueWorkRef(prefix=None, suffix=None).id
        self.assertTrue(pattern_no_prefix_no_suffix.match(ut))

        return

    def test_with_prefix(self):
        random_pref = random.choice(TestUniqueRef.pref)
        pattern_with_prefix = re.compile("^{}-[A-Za-z0-9]+-$".format(random_pref))

        ut = UniqueWorkRef(prefix=random_pref).id
        self.assertTrue(pattern_with_prefix.match(ut))

        ut = UniqueWorkRef(prefix=random_pref, suffix=None).id
        self.assertTrue(pattern_with_prefix.match(ut))
        return

    def test_with_suffix(self):
        random_sufx = random.choice(TestUniqueRef.sufx)
        pattern_with_suffix = re.compile("^-[A-Za-z0-9]+-{}$".format(random_sufx))

        ut = UniqueWorkRef(suffix=random_sufx).id
        self.assertTrue(pattern_with_suffix.match(ut))

        ut = UniqueWorkRef(prefix=None, suffix=random_sufx).id
        self.assertTrue(pattern_with_suffix.match(ut))
        return

    def test_unique(self):
        """
        Generate 10K ref's with random prefix/suffix and ensure ref follows expected pattern
        as well as there being no duplicate references generated.
        """
        have_seen = dict()
        dups = 0
        for _ in range(10000):
            random_pref = random.choice(TestUniqueRef.pref)
            random_sufx = random.choice(TestUniqueRef.sufx)
            if random_pref is None:
                test_pref = ''
            else:
                test_pref = random_pref

            if random_sufx is None:
                test_sufx = ''
            else:
                test_sufx = random_sufx

            test_pattern = re.compile("^{}-[A-Za-z0-9]+-{}$".format(test_pref, test_sufx))
            ut = UniqueWorkRef(prefix=random_pref, suffix=random_sufx).id
            self.assertTrue(test_pattern.match(ut))
            if ut in have_seen:
                dups += 1
            else:
                have_seen[ut] = True
        self.assertTrue(dups == 0)
        return

    @staticmethod
    def _factory() -> UniqueWorkRef:
        """
        Generate a random instance of a UniqueWorkRef
        :return: A new UniqueWorkRef
        """
        return UniqueWorkRef(prefix=random.choice(TestUniqueRef.pref),
                             suffix=random.choice(TestUniqueRef.sufx))

    def test_pubsub_transport(self):
        """
        Generate 1000 random references and ensure that all serialize/deserialize correctly.
        The requires the containerized test Kafka Service to be running locally.
        """
        expected = list()
        actual = list()
        expected, actual = KPuBsubUtil.kpubsub_test(msg_factory=self._factory,
                                                    num_msg=50,
                                                    msg_map_url=kpubsubai.MSG_MAP_URL)
        self.assertTrue(len(expected) == len(actual))
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)
        return


if __name__ == "__main__":
    unittest.main()
