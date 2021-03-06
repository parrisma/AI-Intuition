import logging
import random

from lib.reflrn.interface.Agent import Agent
from lib.reflrn.interface.State import State

from lib.reflrn.stochastic.StochasticActorCriticPolicy import StochasticActorCriticPolicy


class StochasticAgent(Agent):

    def __init__(self,
                 agent_id: int,  # immutable & unique id for this agent
                 agent_name: str,  # immutable & unique name for this agent
                 lg: logging):
        self.lg = lg
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.episode = 0
        self.policy = StochasticActorCriticPolicy(st_size=9,
                                                  a_size=9,
                                                  num_states=6000)
        return

    # Return immutable id
    #
    def id(self):
        return self.agent_id

    # Return immutable name
    #
    def name(self):
        return self.agent_name

    #
    # Environment call back when environment shuts down
    #
    def terminate(self,
                  save_on_terminate: bool = False):
        self.lg.debug(self.agent_name + " Environment Termination Notification")
        return

    #
    # Environment call back when episode starts
    #
    def episode_init(self, state: State):
        self.lg.debug(self.agent_name + " Episode Initialisation Notification  : ")
        self.episode += 1
        return

    #
    # Environment call back when episode is completed
    #
    def episode_complete(self, state: State):
        self.lg.debug(self.agent_name + " Episode Complete Notification  : ")
        return

    #
    # Environment call back to ask the agent to chose an action
    #
    # State : The current representation of the environment
    # possible_actions : The set of possible actions the agent can play from this curr_coords
    #
    def chose_action(self, state: State, possible_actions: [int]) -> int:
        action = -1
        guess = 0
        while (action not in possible_actions) and guess < 5:
            action, _ = self.policy.act(state, self.episode)
            guess += 1
        if guess >= 5:
            action = random.choice(possible_actions)
        return action

    def predict(self, state: State) -> None:
        """
        Show the probability of winning by action for the given state
        :param state: The State to predict for
        :return:
        """
        print(str(self.policy.actor_model.predict(state.state_model_input(), batch_size=1).flatten()))
        return

    # Environment call back to reward agent for a play chosen for the given
    # state passed.
    #
    def reward(self, state: State, next_state: State, action: int, reward_for_play: float, episode_complete: bool):
        self.lg.debug(self.agent_name + " reward  : " + str(reward_for_play) + " for action " + str(action))
        self.policy.remember(state=state,
                             action=action,
                             r=reward_for_play,
                             next_state=next_state)
        if episode_complete:
            self.lg.debug(self.agent_name + " Episode Completed")
        return

    #
    # Called by the environment *once* at the start of the session
    # and the action set is given as dictionary
    #
    def session_init(self,
                     actions: dict) -> None:
        self.lg.debug(self.agent_name + " Session Initialisation Notification  : ")
        return

    #
    # Produce debug details when performing operations such as action prediction.
    #
    @property
    def explain(self) -> bool:
        raise NotImplementedError()

    @explain.setter
    def explain(self, value: bool):
        raise NotImplementedError()
