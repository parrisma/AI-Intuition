import math
import random
from collections import deque
from typing import Tuple

import numpy as np
import keras.backend as K
from keras.initializers import RandomUniform
from keras.initializers import Zeros
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import multi_gpu_model
from lib.reflrn.common.SimpleLearningRate import SimpleLearningRate
from lib.reflrn.interface.State import State


#
# Two network actor / critic stochastic policy with the critic learning state q-values on a one step Bellman.
#
# Exploration is inherent as policy is stochastic
#
class StochasticActorCriticPolicy:
    """
    Implementation of a reinforcement learning agent.

    The agent follows an actor-critic pattern and makes use of a reply buffer.

    Critic: a neural network that learns Action Values
    Actor: a neural network that learns a probability distribution over the finite action set.

    param: st_size - the dimension of the state space
    param: a_size - the dimension of the action space
    num_states: - an estimate of the total number of states in the state space

    """
    __seed = 42

    def __init__(self,
                 st_size,
                 a_size,
                 num_states):

        self.num_gpu = 2
        self.state_size = st_size
        self.action_size = a_size
        self.num_states = num_states

        self.uniform_prob = np.full((self.action_size), 1.0 / self.action_size)

        self.gamma = 0.99
        self.learning_rate = 0.001
        self.replay = deque(maxlen=300)
        self.replay_kl_factor = 0.0
        self.kl_update = 0
        self.actor_model = self._build_actor_model()
        self.critic_model = self._build_critic_model()

        self.actor_model.summary()

        self.critic_model.summary()
        qval_lr0 = float(1)
        self.qval_learning_rate = SimpleLearningRate(lr0=qval_lr0,
                                                     lrd=SimpleLearningRate.lr_decay_target(learning_rate_zero=qval_lr0,
                                                                                            target_step=5000,
                                                                                            target_learning_rate=0.01),
                                                     lr_min=0.01)

        self.state_dp = 5
        self.critic_loss_history = []
        self.actor_loss_history = []
        self.critic_acc_history = []
        self.actor_acc_history = []
        self.actor_exploration_history = []

        self.critic_updates = 0

        return

    def visualise(self) -> str:
        """
        Return a printable view of the current state of the agent & it's internals.
        :return: printable view as a string.
        """
        return self.visual

    def replay_kl(self):
        """
        A view of the bias in the replay memory as a simple variant of the Kullback–Leibler divergence
        between an even distribution and current distribution
        :return: a numerical factor of the divergence
        """
        dl = 0
        sd = dict()
        for s in self.replay:
            state, _, _, _ = s
            state = np.array2string(state[0])
            if state in sd:
                sd[state] += 1
            else:
                sd[state] = 1
            dl += 1
        if dl < 2:
            return 0
        qx = ((dl / len(sd)) / dl)
        kln = math.log(1.0 / qx)
        kls = 0.0
        u = 0.0
        c = 0
        for k, v in sd.items():
            px = v / dl
            u += px * math.log(max(px, 1e-12) / max(qx, 1e-12))
            if u > 0:
                kls += u
                c += 1
            # print('k:{:d} v:{:d} px:{:f} qx:{:f} u:{:f} kls:{:f}'.format(k, v, px, qx, u, kls))
        klp = (kls / c) / kln
        return klp

    def _build_actor_model(self):
        """
        Simple fully connected network to learn the probability distribution over the action space where the
        most profitable action as defined by the critic will have the highest probability.

        :return: a Keras model capable of learning the probability distribution of a state space of approx 10K with
        and action space of 5 - 10
        """
        ki = RandomUniform(minval=-0.05, maxval=0.05, seed=self.__seed)
        bi = Zeros()
        model = Sequential()
        model.add(Dense(800, input_dim=self.state_size, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        model.add(Dropout(0.1))
        model.add(Dense(400, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        model.add(Dropout(0.1))
        model.add(Dense(200, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        model.add(Dropout(0.05))
        model.add(Dense(units=self.action_size, activation='linear', kernel_initializer=ki, bias_initializer=bi))
        if self.num_gpu > 0:
            model = multi_gpu_model(model, gpus=self.num_gpu)

        def custom_loss(y_true, y_pred):
            return K.sum(K.mean(K.square(y_pred - y_true), axis=-1)) + K.abs(1 - K.sum(y_pred))

        model.compile(loss=custom_loss,  # 'mean_squared_error',
                      optimizer=Adam(lr=self.learning_rate),
                      metrics=['accuracy']
                      )
        return model

    def _build_critic_model(self):
        """
        Simple fully connected network to learn action values for the actions in teh state space.

        :return: a Keras model capable of learning the action values of a state space of approx 10K with
        and action space of 5 - 10
        """
        ki = RandomUniform(minval=-0.05, maxval=0.05, seed=self.__seed)
        bi = Zeros()
        model = Sequential()
        model.add(Dense(800, input_dim=self.state_size, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        model.add(Dropout(0.1))
        model.add(Dense(400, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        model.add(Dropout(0.1))
        model.add(Dense(200, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        model.add(Dropout(0.05))
        model.add(Dense(units=self.action_size, activation='linear', kernel_initializer=ki, bias_initializer=bi))
        if self.num_gpu > 0:
            model = multi_gpu_model(model, gpus=self.num_gpu)
        model.compile(loss='mean_squared_error',
                      optimizer=Adam(lr=self.learning_rate),
                      metrics=['accuracy']
                      )
        return model

    def remember(self,
                 state: State,
                 action,
                 r: float,
                 next_state: State) -> None:
        """
        Update the playback memory with the given State-Action-Reward set
        :param state: Current State
        :param action: Current Action
        :param r: Current reward for given action in given state
        :param next_state: the state transitioned to for the given starting State-Action pair
        :return: None
        """
        y = np.zeros([self.action_size])
        y[action] = 1  # One hot encode.
        self.replay.append([StochasticActorCriticPolicy.state_model_input(state=state),
                            np.array(y).astype('float32'),
                            r,
                            StochasticActorCriticPolicy.state_model_input(state=next_state)])
        # Update the stats on the current bias of the reply memory
        if self.kl_update % 250 == 0:
            self.replay_kl_factor = self.replay_kl()
            self.kl_update = 0
        self.kl_update += 1
        return

    def train_agent(self,
                    episode: int) -> None:
        """
        Given the current episode retrain the critic and/or the actor.
        :param episode: The current episode
        :return: None
        """
        if episode % 10 == 0:
            self.train_critic(episode)
            self.critic_updates += 1

        if self.critic_updates == 3:
            self.train_actor()
            self.critic_updates = 0

        return

    def act(self,
            state: State,
            episode: int) -> Tuple[int, float]:
        """
        Suggest an action based on the currently learned (stochastic) policy
        :param state: Current State
        :param episode: Current Episode
        :return: predicted action, bias-factor
        """
        state = StochasticActorCriticPolicy.state_model_input(state=state)
        klf = self.replay_kl_factor
        aprob = self.actor_model.predict(state, batch_size=1).flatten()
        aprob[aprob < 0.0] = 0.0
        if np.sum(aprob) == 0:
            aprob = self.uniform_prob
        else:
            aprob = ((1 - klf) * aprob) + (klf * self.uniform_prob)
            aprob /= np.sum(aprob)
        action = np.random.choice(self.action_size, 1, p=aprob)[0]

        # Make a decision on retaining actor/critic
        self.train_agent(episode)

        return action, klf

    def qval_lr(self,
                episode: int) -> float:
        """
        Learning rate to apply for the given q-value update
        :param episode: the number of the current episode
        :return: the learning rate to apply
        """
        return self.qval_learning_rate.learning_rate(episode)

    def train_critic(self,
                     episode: int) -> Tuple[float, float]:
        """
        Take a random sample from the reply buffer and create a current set of training data from which to
        run a learning cycle for the critic network
        :param episode: current episode
        :return: training loss, training accuracy
        """
        batch_size = min(len(self.replay), 250)
        X = np.zeros((batch_size, self.action_size))
        Y = np.zeros((batch_size, self.action_size))
        samples = random.sample(list(self.replay), batch_size)
        i = 0
        for sample in samples:
            state, action_one_hot, reward, next_state = sample
            lr = self.qval_lr(episode)
            action_value_s = self.critic_model.predict(state, batch_size=1).flatten()
            action_value_ns = self.critic_model.predict(next_state, batch_size=1).flatten()
            qv_s = action_one_hot * action_value_s
            qv_ns = np.max(action_value_ns)  # * self.gamma
            av = (reward + (qv_ns * self.gamma)) - np.max(action_value_s)
            # TODO av = ((qv_s * (1 - lr)) + (lr * (reward + qv_ns))) - np.max(action_value_s)
            qv_u = (action_value_s * (1 - action_one_hot)) + (av * action_one_hot)
            X[i] = np.squeeze(state)
            Y[i] = np.squeeze(qv_u)
            i += 1
        ls, acc = self.critic_model.train_on_batch(X, Y)
        print("Critic Training: episode [{:d}] - [{:f} - {:f}]".format(episode, ls, acc))
        return ls, acc

    #
    # Train the actor to learn the stochastic policy; the reward is the reward for the action
    # as predicted by the critic.
    #
    def train_actor(self) -> Tuple[float, float]:
        """
        Take a random sample from the replay buffer. Ask the current critic network to create up to date
        predictions and then create a training data set for the actor.

        :return: training loss, training accuracy
        """
        #  ToDo: Leanring Rate Decay by Episode ?
        batch_size = min(len(self.replay), 250)
        X = np.zeros((batch_size, self.state_size))
        Y = np.zeros((batch_size, self.action_size))
        samples = random.sample(list(self.replay), batch_size)
        i = 0
        for sample in samples:
            state, action_one_hot, reward, next_state = sample
            action_value_s = self.critic_model.predict(state, batch_size=1).flatten()
            action_probs_s = self.actor_model.predict(state, batch_size=1).flatten()

            avn = ((1 - action_one_hot) * action_value_s) + (action_one_hot * reward)
            avn -= np.max(avn)
            avn /= np.abs(np.sum(avn))

            action_probs_s[action_probs_s <= 0.0] = 0.01  # min % chance = 1%
            action_probs_s /= np.sum(action_probs_s)
            action_probs_s += (action_probs_s * avn * 0.7)
            action_probs_s /= np.sum(action_probs_s)

            X[i] = state
            Y[i] = action_probs_s
            i += 1
        ls, acc = self.actor_model.train_on_batch(X, Y)
        print("Actor Training: loss [{:f}] accuracy [{:f}]".format(ls, acc))
        return ls, acc

    def load(self, name) -> None:
        """
        Load the actor & critic weights
        :param name: the root of the filename to load the weights from
        :return:
        """
        self.actor_model.load_weights('actor' + name)
        self.critic_model.load_weights('critic' + name)

    def save(self, name) -> None:
        """
        Save the actor & critic weights
        :param name: the root of the filename to save weights as
        :return:
        """
        self.actor_model.save_weights('actor' + name)
        self.critic_model.save_weights('critic' + name)

    @classmethod
    def state_model_input(cls, state: State) -> np.ndarray:
        """
        Convert the state to the tensor form needed for model inout
        :param state: State object
        :return: state as numpy array
        """
        st = state.state_as_array()
        st = st.reshape([1, 9])
        return st

    # Simple debugger output - could be refactored into PBFunc env as it is more env specific ?
    #
    def print_progress(self) -> None:
        self.actor_loss_history = self.actor_loss_history[-500:]
        self.critic_loss_history = self.critic_loss_history[-500:]
        self.actor_acc_history = self.actor_acc_history[-500:]
        self.critic_acc_history = self.critic_acc_history[-500:]
        self.actor_exploration_history = self.actor_exploration_history[-500:]

        # self.visualise().plot_loss_function(actor_loss=self.actor_loss_history,
        #                                    critic_loss=self.critic_loss_history)

        # self.visualise().plot_acc_function(actor_acc=self.actor_acc_history,
        #                                   critic_acc=self.critic_acc_history,
        #                                   exploration=self.actor_exploration_history)

        # self.visualise().plot_qvals_function(states=states,
        #                                     qvalues_action1=predicted_qval_action1,
        #                                     qvalues_action2=predicted_qval_action2,
        #                                     qvalues_reference=replay_qvals)

        # self.visualise().plot_prob_function(states=states,
        #                                    action1_probs=predicted_prob_action1,
        #                                    action2_probs=predicted_prob_action2)

        return
