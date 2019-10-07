import numpy as np
from keras.initializers import RandomUniform
from keras.optimizers import Adam
from keras import backend as K
from keras.layers import Input, Dense, BatchNormalization
from keras.models import Model
from keras.utils import multi_gpu_model
from keras.metrics import kullback_leibler_divergence
import matplotlib.pyplot as plt
import datetime
import math


class QValNeuralNet:
    """
    An experimental class to see if we can learn a set of QValues for a given action space.

    This is tuned to the TicTacToe problem where we have a state space of about 5K and nine actions.

    We create a test data set based on 5K random states [O, X, <blank>] = [0,1,2] and for each of the create
    and arbitrary qvalue set of the action space. Typically we aim to calculate qvalue so that it is in a
    small range around 1.0 but there is no constraint on the range or sum of qvalues for a given state

    We then simulate a number of test modes for learning this pdf.

    1. A single episode where all 5K states are iterated over for a large number of epochs
    2. Many (sample) episodes over many episodes :
        just a sample of the total state space is seen each episode
        this models the RL pattern with a reply buffer
    3. Same as case 2. above but with a noise factor
        the noise simulates the evolving pdf as the actor learns from critic feedback
        we start at near 100% noise and decay to 5% noise
    """
    test_set_size = 1500
    seed = 42.0
    state_size = 9  # Nine board spaces ( 3 x 3)
    action_size = 9  # (max) Nine possible actions for a given state
    num_gpu = 2  # How many GPU's do you have ?
    eps = 1e-09

    def __init__(self):
        self.learning_rate = 0.005  # 0.0025 We don't take the default adam LR we use this as a tuned hyper param.

    def build_qval_model(self):
        """
        Simple fully connected network to learn the Q-Values over the action space where the
        most profitable action as defined by the critic will have the highest Q-Value.

        The network is working as a regression: learning the QValues over the action space and as such has a custom
        loss function with a constraint that the prediction sum to 1.0

        :return: a Keras model capable of learning the Q-Values of a state space of approx 5K with
        and action space of 9
        """
        ki = RandomUniform(minval=-0.05, maxval=0.05, seed=self.seed)
        bi = RandomUniform(minval=-0.05, maxval=0.05, seed=self.seed)

        qval_in = Input(shape=(self.state_size,), name="qval_in")
        qval_l1 = Dense(2000, activation='relu')(qval_in)
        qval_l2 = Dense(10000, activation='relu')(qval_l1)
        qval_l5 = Dense(2000, activation='relu')(qval_l2)
        qval_out = Dense(units=self.action_size, activation='linear')(qval_l5)

        qval_model = Model(inputs=qval_in, outputs=qval_out)

        if self.num_gpu > 0:
            qval_model = multi_gpu_model(qval_model, gpus=self.num_gpu)

        qval_model.compile(loss='mse',
                           optimizer=Adam(lr=self.learning_rate),
                           metrics=['mse']
                           )

        print(qval_model.summary())

        return qval_model

    @classmethod
    def plot_results(cls,
                     loss_history,
                     validation_loss_history,
                     num_epochs,
                     skip=50):
        """

        :param loss_history:
        :param validation_loss_history:
        :param num_epochs: x axis dimension - how many losses
        :param skip: how many points to ignore at the start of the loss history (when it is large and unstable)
        :return:
        """
        color_r = 'tab:red'
        color_b = 'tab:blue'

        sh = (num_epochs - skip)
        sh = num_epochs if sh < 0 else sh
        h_loss = np.asarray(loss_history[-sh:])
        h_v_loss = np.asarray(validation_loss_history[-sh:])
        epocs = np.arange(sh)

        print(h_loss.shape)
        print(epocs.shape)

        fig, _ = plt.subplots(figsize=(15, 6))

        ax1 = plt.subplot(1, 1, 1)
        plt.title('Loss')
        ax1.set_xlabel('Epoc')
        ax1.set_ylabel('Traing Loss', color=color_r)
        ax1.plot(epocs, h_loss, color=color_r)
        ax1.tick_params(axis='y', labelcolor=color_r)
        ax2 = ax1.twinx()  # 2nd Axis for Validation Loss
        ax2.set_ylabel('Validation Loss', color=color_b)
        ax2.plot(epocs, h_v_loss, color=color_b)
        ax2.tick_params(axis='y', labelcolor=color_b)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()
        return

    @classmethod
    def generate_qvl_training_data(cls):
        """
        For a randomly generated state generate a randomly generated q-values over the action space. In fact we
        calc the action value by subtracting the max qvalue from the set.
        :return: states, corresponding qvals's
        """
        sz = cls.test_set_size
        _x = np.zeros((sz, cls.state_size))
        _y = np.zeros((sz, cls.action_size))
        u = dict()
        u[str(_x[0])] = True
        for _i in range(0, sz):
            _qval = np.random.random((cls.action_size))
            _qval = (_qval * 2.0) - 1.0
            _x[_i] = np.random.randint(3, size=cls.action_size)
            while str(_x[_i]) in u:
                _x[_i] = np.random.randint(3, size=cls.action_size)
            u[str(_x[_i])] = True
            _y[_i] = _qval
        return _x, _y

    @classmethod
    def single_pass(cls):
        """
        :return: batch size ; num epochs ; num episodes, training set size
        """
        return 64, 2500, 1, cls.test_set_size, 0.0, 0.0

    @classmethod
    def multi_pass(cls):
        """
        :return: batch size ; num epochs ; training set size
        """
        # return 64, 20, 1000, int(cls.test_set_size * 0.1), 1.0, 0.005  # ToDo epochs should be 2000
        # return 64, 20, 500, int(cls.test_set_size * 0.1), 1.0, 0.00001  # ToDo epochs should be 2000
        return 64, 20, 500, int(cls.test_set_size * 0.1), 0.0, 0.0

    @classmethod
    def noise_factor(cls,
                     epoch,
                     max_epoch,
                     max_noise,
                     min_noise):
        """
        Return an exponentially reducing noise factor given the current epoch
        :param epoch: current epoch
        :param max_epoch: the total number of epochs in the training
        :param max_noise: man noise as a % e.g. 1 = 100% noise
        :param min_noise: min noise as a % e.g 0 = 0% noise
        :return: the noise factor
        """
        mxn = min(cls.eps, max_noise)
        mnn = min(cls.eps, min_noise)
        ns = (math.log(mxn) - math.log(mnn)) / (1 - max_epoch)
        return max_noise * math.exp(-(ns * epoch))

    @classmethod
    def train(cls,
              training,
              qval_model,
              t_x,
              t_y):
        """
        Run a training simulation on the given test state & pdf space.
        :param training - function thar returns the training set-up
        :param qval_model: - a Keras model that will learn state -> pdf
        :param t_x: training state data
        :param t_y: training pdf data
        :return: none
        """
        batch_size, num_epochs, num_episodes, samples, max_noise, min_noise = training()

        h_l = None
        h_vl = None

        idx = np.arange(cls.test_set_size)
        np.random.shuffle(idx)
        idx = idx[:samples]

        s_x = t_x[idx]
        s_y = t_y[idx]
        for i in range(0, num_episodes):
            print('>>>>>')
            print('EPISODE: ' + str(i))
            if max_noise > 0:
                sp = np.shape(s_y)
                s_y_r = np.random.rand(sp[0], sp[1])
                s_y_n = s_y * s_y_r * cls.noise_factor(epoch=i,
                                                       max_epoch=num_episodes,
                                                       max_noise=max_noise,
                                                       min_noise=min_noise)
                s_y_n = s_y + ((s_y / 2.0) - s_y_n)
            else:
                s_y_n = s_y

            history = qval_model.fit(s_x,
                                     s_y_n,
                                     epochs=num_epochs,
                                     batch_size=batch_size,
                                     shuffle=True,
                                     validation_split=0.15,
                                     verbose=2
                                     )
            hl = history.history['loss']
            hv = history.history['val_loss']
            if h_l is None:
                h_l = hl
                h_vl = hv
            else:
                h_l = h_l + hl
                h_vl = h_vl + hv

            _p = np.zeros((1, cls.action_size))
            _p[0] = s_x[0]
            pr = model.predict(_p)
            print('<<<<<')

        cls.plot_results(h_l, h_vl, (num_epochs * (i + 1)))
        cls.save_hist(history)
        return

    @classmethod
    def save_hist(cls,
                  history):
        """
        Takes a keras history dictionary and saves as a CSV with each of the history items as a column
        :param history: Keras history dict
        """

        new_hist = {}
        for key in list(history.history.keys()):
            if type(history.history[key]) == np.ndarray:
                new_hist[key] == history.history[key].tolist()
            elif type(history.history[key]) == list:
                if type(history.history[key][0]) == np.float64:
                    new_hist[key] = list(map(float, history.history[key]))

        tmst = datetime.datetime.now().strftime('%d-%b-%Y-%H_%M_%S_%f')
        np.savetxt(fname='./saved_hist/history-' + tmst + '.csv',
                   X=(np.array([new_hist[k] for k in new_hist.keys()])).transpose(),
                   newline='\n',
                   delimiter=',',
                   fmt='%0.8f',
                   header=','.join(list(new_hist.keys())),
                   comments='',
                   encoding='utf-8')
        return


#
# Run a training simulation.
#
if __name__ == "__main__":
    pdf = QValNeuralNet()
    model = pdf.build_qval_model()
    x, y = pdf.generate_qvl_training_data()
    pdf.train(QValNeuralNet.single_pass,
              model,
              x,
              y)

    #
    # Generate a test set and see how well the model learned.
    #
    test = np.random.randint(QValNeuralNet.test_set_size, size=20)
    _pr = np.zeros((1, QValNeuralNet.action_size))
    for i in test:
        _pr[0] = x[i]
        print('-----------------------')
        print('Yo: ' + str(y[i]))
        pr = model.predict(_pr)
        print('Yp: ' + str(pr))
        print('1: ' + str(np.sum(pr)))
        print('Err: ' + str(y[i] - pr))
