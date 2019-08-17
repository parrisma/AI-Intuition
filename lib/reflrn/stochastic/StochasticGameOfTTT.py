import logging
import unittest

from lib.reflrn.ttt.TicTacToe import TicTacToe
from lib.reflrn.ttt.TicTacToeLogging import TicTacToeLogging
from lib.reflrn.test.TestAgent import TestAgent

from lib.reflrn.stochastic.StochasticAgent import StochasticAgent
from lib.reflrn.ttt.TicTacToeState import TicTacToeState


class BasicGameWithTestAgents(unittest.TestCase):
    def test_ten_random_games(self):
        try:
            lg = TicTacToeLogging("StochasticActorCriticPolicy", "StochasticActorCriticPolicy.log",
                                  logging.DEBUG).get_logger()
            actor_x = StochasticAgent(agent_id=1, agent_name='X', lg=lg)
            actor_o = TestAgent(agent_id=0, agent_name='O', lg=lg)
            ttt_game = TicTacToe(x=actor_x, o=actor_o, lg=lg)
            ttt_game.run(iterations=1000)
            ttt_game.show_summary()

            s = TicTacToeState(None, actor_x, actor_o)
            s.init_from_string('.........')
            actor_x.predict(s)
            s.init_from_string('100.....1')
            actor_x.predict(s)


        except:
            self.fail("Run of stochastic actor critic failed!")
        return


if __name__ == "__main__":
    tests = BasicGameWithTestAgents()
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner().run(suite)
