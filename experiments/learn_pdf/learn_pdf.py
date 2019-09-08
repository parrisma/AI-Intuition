import numpy as np
from keras.initializers import RandomUniform
from keras.optimizers import Adam
from keras import backend as K
from keras.layers import Input, Dense, Dropout, BatchNormalization, Activation, LeakyReLU
from keras.models import Model
from keras.utils import multi_gpu_model
from keras.metrics import kullback_leibler_divergence
import matplotlib.pyplot as plt
import json
import codecs


class PDFNeuralNet:
    """
    An experimental class to see if we can learn a probability density function that represents the probability
    of the most successful action in a given state.

    This is tuned to the TicTacToe problem where we have a state space of about 5K and nine actions.

    We create a test data set based on 5K random states [O, X, <blank>] = [0,1,2] and for each of the create
    and arbitrary action pdf.

    We then simulate a number of test modes for learning this pdf.

    1. A single episode where all 5K states are iterated over for a large number of epochs
    2. Many (sample) episodes over many episodes :
        just a sample of the total state space is seen each episode
        this models the RL pattern with a reply buffer
    3. Same as case 2. above but with a noise factor
        the noise simulates the evolving pdf as the actor learns from critic feedback
        we start at near 100% noise and decay to 5% noise
    """
    test_set_size = 5000
    seed = 42.0
    state_size = 9  # Nine board spaces ( 3 x 3)
    action_size = 9  # (max) Nine possible actions for a given state
    num_gpu = 2  # How many GPU's do you have ?
    eps = 1e-09

    def __init__(self):
        self.learning_rate = 0.0025  # 0.0025 We don't take the default adam LR we use this as a tuned hyper param.

    def build_pdf_model(self):
        """
        Simple fully connected network to learn the probability distribution over the action space where the
        most profitable action as defined by the critic will have the highest probability.

        The network is working as a regression: learning the pdf over the action space and as such has a custom
        loss function with a constraint that the prediction sum to 1.0

        :return: a Keras model capable of learning the probability distribution of a state space of approx 5K with
        and action space of 9
        """
        ki = RandomUniform(minval=-0.05, maxval=0.05, seed=self.seed)
        bi = RandomUniform(minval=-0.05, maxval=0.05, seed=self.seed)

        pdf_in = Input(shape=(self.state_size,), name="pdf_in")
        pdf_l1 = Dense(100, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_in)
        pdf_l2 = Dense(400, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l1)
        pdf_l3 = Dense(1600, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l2)
        pdf_l4 = Dense(800, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l3)
        pdf_l5 = Dense(200, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l4)
        pdf_l6 = Dense(100, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l5)
        pdf_l7 = Dense(50, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l6)
        pdf_out = Dense(units=self.action_size, activation='linear')(pdf_l7)

        pdf_model = Model(inputs=pdf_in, outputs=pdf_out)

        if self.num_gpu > 0:
            pdf_model = multi_gpu_model(pdf_model, gpus=self.num_gpu)

        def mse_pdf(y_true, y_pred):
            """
            A modified mse loss function that constrains predictions to sum to 1.0 as we are
            learning a pdf over the given action space.
            :param y_true: target tensor
            :param y_pred: prediction tensor
            :return: loss (mse + squared diff w.r.t 1.0)
            """
            mse = K.mean(K.square(y_true - y_pred), axis=-1)
            sum_constraint = K.square(K.sum(y_pred, axis=-1) - 1)
            return mse + sum_constraint

        pdf_model.compile(loss=mse_pdf,
                          optimizer=Adam(lr=self.learning_rate),
                          metrics=[kullback_leibler_divergence]
                          )

        print(pdf_model.summary())

        return pdf_model

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

        sh = min(num_epochs, (num_epochs - skip))
        h_loss = np.asarray(loss_history[-sh:])
        h_v_loss = np.asarray(validation_loss_history[-sh:])
        epocs = np.arange(sh)

        print(h_loss.shape)
        print(epocs.shape)

        fig, _ = plt.subplots(figsize=(15, 6))

        # Loss
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
    def generate_pdf_training_data(cls):
        """
        For a randomly generated state generate a randomly generated pdf over the action space
        :return: states, corresponding pdf's
        """
        sz = cls.test_set_size
        _x = np.zeros((sz, cls.state_size))
        _y = np.zeros((sz, cls.action_size))
        u = dict()
        u[str(_x[0])] = True
        for _i in range(0, sz):
            _pdf = np.random.randint(100, size=cls.action_size)
            _pdf = _pdf / np.sum(_pdf)
            _x[_i] = np.random.randint(3, size=cls.action_size)
            while str(_x[_i]) in u:
                _x[_i] = np.random.randint(3, size=cls.action_size)
            u[str(_x[_i])] = True
            _y[_i] = _pdf
        return _x, _y

    @classmethod
    def kld(cls,
            y_true,
            y_pred):
        """
        Calculate the kullback leibler divergence
        :param y_true: target pdf
        :param y_pred: predicited pdf
        :return: The KL Divergence
        """
        y_pred /= np.sum(y_pred)
        y_true = np.clip(y_true, cls.eps, 1)
        y_pred = np.clip(y_pred, cls.eps, 1)
        print(y_pred)
        print(y_true)
        print(y_true * np.log(y_true / y_pred))
        _kld = np.sum(y_true * np.log(y_true / y_pred), axis=-1)
        print('KLD: ' + str(_kld))
        return _kld

    @classmethod
    def single_pass(cls):
        """
        :return: batch size ; num epochs ; num episodes, training set size
        """
        return 64, 20, 1, cls.test_set_size

    @classmethod
    def multi_pass(cls):
        """
        :return: batch size ; num epochs ; training set size
        """
        return 64, 20, 1000, int(cls.test_set_size * 0.1)

    @classmethod
    def train(cls,
              training,
              pdf_model,
              t_x,
              t_y):
        """
        Run a training simulation on the given test state & pdf space.
        :param training - function thar returns the training set-up
        :param pdf_model: - a Keras model that will learn state -> pdf
        :param t_x: training state data
        :param t_y: training pdf data
        :return: none
        """
        batch_size, num_epochs, num_episodes, samples = training()

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
            history = pdf_model.fit(s_x,
                                    s_y,
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
            cls.kld(s_y[0], pr)
            print('<<<<<')

        cls.plot_results(h_l, h_vl, (num_epochs * (i + 1)))
        cls.save_hist('hst', history)
        return

    @classmethod
    def save_hist(cls,
                  path,
                  history):
        new_hist = {}
        for key in list(history.history.keys()):
            if type(history.history[key]) == np.ndarray:
                new_hist[key] == history.history[key].tolist()
            elif type(history.history[key]) == list:
                if type(history.history[key][0]) == np.float64:
                    new_hist[key] = list(map(float, history.history[key]))

        print(new_hist)
        with codecs.open(path, 'w', encoding='utf-8') as f:
            json.dump(new_hist, f, separators=(',', ':'), sort_keys=True, indent=4)

    @classmethod
    def load_hist(cls,
                  path):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            n = json.loads(f.read())
        return n


#
# Run a training simulation.
#
if __name__ == "__main__":
    pdf = PDFNeuralNet()
    model = pdf.build_pdf_model()
    x, y = pdf.generate_pdf_training_data()
    pdf.train(PDFNeuralNet.single_pass,
              model,
              x,
              y)

    #
    # Generate a test set and see how well the model learned.
    #
    test = np.random.randint(PDFNeuralNet.test_set_size, size=20)
    _pr = np.zeros((1, PDFNeuralNet.action_size))
    for i in test:
        _pr[0] = x[i]
        print('-----------------------')
        print('Yo: ' + str(y[i]))
        pr = model.predict(_pr)
        print('Yp: ' + str(pr))
        print('1: ' + str(np.sum(pr)))
        print('Err: ' + str(y[i] - pr))
        print('KLD:' + str(PDFNeuralNet.kld(y[i], pr)))
