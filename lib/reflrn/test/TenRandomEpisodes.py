import logging
import unittest

from lib.reflrn.ttt.TicTacToe import TicTacToe
from lib.reflrn.ttt.TicTacToeLogging import TicTacToeLogging
from lib.reflrn.test.TestAgent import TestAgent


class BasicGameWithTestAgents(unittest.TestCase):
    def test_ten_random_games(self):
        try:
            lg = TicTacToeLogging("TenRandomEpisodes", "TenRandomEpisodes.log", logging.DEBUG).get_logger()
            actor_x = TestAgent(agent_id=1, agent_name='X', lg=lg)
            actor_o = TestAgent(agent_id=0, agent_name='O', lg=lg)
            ttt_game = TicTacToe(x=actor_x, o=actor_o, lg=lg)
            ttt_game.run(iterations=10)
        except:
            self.fail("Run of 10 simple random games failed!")
        return


if __name__ == "__main__":
    tests = BasicGameWithTestAgents()
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner().run(suite)
