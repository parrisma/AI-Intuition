import unittest
from typing import List
from journey11.src.lib.state import State
from journey11.src.lib.loggingsetup import LoggingSetup


class TestState(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def test_range_asc(self):
        scenarios = [[State.S0, State.S0, [State.S0]],
                     [State.S9, State.S9, [State.S9]],
                     [State.S5, State.S5, [State.S5]],
                     [State.S0, State.S1, [State.S0, State.S1]],
                     [State.S8, State.S9, [State.S8, State.S9]],
                     [State.S5, State.S6, [State.S5, State.S6]],
                     [State.S2, State.S5, [State.S2, State.S3, State.S4, State.S5]],
                     [State.S1, State.S0, [State.S1, State.S0]],
                     [State.S8, State.S4, [State.S8, State.S7, State.S6, State.S5, State.S4]]
                     ]
        for st, ed, expected in scenarios:
            self.run_state_scenario(st, ed, expected)
        return

    def run_state_scenario(self,
                           st: State,
                           ed: State,
                           expected: List[State]):
        actual = State.range(st, ed)
        i = 0
        for e in expected:
            self.assertEqual(e, actual[i])
            i += 1
        return

    def test_state_add(self):
        scenarios = [[State.S0, 1, State.S1],
                     [State.S0, 0, State.S0],
                     [State.S0, 9, State.S9],
                     [State.S0, 10, State.S9],
                     [State.S0, -1, State.S0],
                     [State.S1, -1, State.S0],
                     [State.S9, -9, State.S0],
                     [State.S9, -10, State.S0]
                     ]

        for p1, p2, expected in scenarios:
            s = p1 + p2
            self.assertEqual(s, expected)

        for p1, p2, expected in scenarios:
            s = p2 + p1
            self.assertEqual(s, expected)

        self.assertRaises(ValueError, State.__add__, State.S0, str(1))
        self.assertRaises(ValueError, State.__add__, str(1), State.S0)

        return


if __name__ == '__main__':
    unittest.main()
