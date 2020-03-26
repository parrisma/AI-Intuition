import unittest
from typing import List
from journey11.lib.state import State


class TestState(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
