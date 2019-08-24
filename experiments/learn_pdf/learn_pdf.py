import numpy as np
from keras.initializers import RandomUniform
from keras.initializers import Zeros
from keras.optimizers import Adam
from keras import backend as K
from keras.layers import Input, Dense, Dropout, BatchNormalization
from keras.models import Model
from keras.utils import multi_gpu_model
import matplotlib.pyplot as plt

from lib.reflrn.interface.State import State


class PDFNeuralNet:
    test_set_size = 5000

    def __init__(self):
        self.seed = 42.0
        self.state_size = 9
        self.action_size = 9
        self.num_gpu = 2
        self.learning_rate = 0.0025

    def build_pdf_model(self):
        """
        Simple fully connected network to learn the probability distribution over the action space where the
        most profitable action as defined by the critic will have the highest probability.

        :return: a Keras model capable of learning the probability distribution of a state space of approx 10K with
        and action space of 5 - 10
        """
        ki = RandomUniform(minval=-0.05, maxval=0.05, seed=self.seed)
        bi = RandomUniform(minval=-0.05, maxval=0.05, seed=self.seed)  # Zeros()

        pdf_in = Input(shape=(self.state_size,), name="pdf_in")
        pdf_l1 = Dense(100, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_in)
        pdf_l2 = Dense(400, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l1)
        pdf_l3 = Dense(1600, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l2)
        pdf_l4 = Dense(800, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l3)
        pdf_l5 = Dense(200, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l4)
        pdf_l6 = Dense(100, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l5)
        pdf_l7 = Dense(50, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l6)
        pdf_out = Dense(units=self.action_size, activation='linear')(pdf_l7)

        pdf_model = Model(inputs=[pdf_in], outputs=[pdf_out])

        if self.num_gpu > 0:
            pdf_model = multi_gpu_model(pdf_model, gpus=self.num_gpu)

        def custom_loss1(y_true, y_pred):
            mse = K.mean(K.square(y_true - y_pred), axis=-1)
            sum_constraint = K.square(K.sum(y_pred, axis=-1) - 1)
            return mse + sum_constraint

        pdf_model.compile(loss=custom_loss1,
                          optimizer=Adam(lr=self.learning_rate),
                          metrics=[custom_loss1]
                          )

        print(pdf_model.summary())

        return pdf_model

    @classmethod
    def plot_results(cls,
                     loss_history,
                     validation_loss_history,
                     num_epochs,
                     skip=150):
        color_r = 'tab:red'
        color_b = 'tab:blue'

        sh = max(num_epochs, (num_epochs - skip))
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
        sz = cls.test_set_size
        _x = np.zeros((sz, 9))
        _y = np.zeros((sz, 9))
        u = dict()
        u[str(_x[0])] = True
        for _i in range(0, sz):
            _pdf = np.random.randint(100, size=9)
            _pdf = _pdf / np.sum(_pdf)
            _x[_i] = np.random.randint(3, size=9)
            while str(_x[_i]) in u:
                _x[_i] = np.random.randint(3, size=9)
            u[str(_x[_i])] = True
            _y[_i] = _pdf
        return _x, _y

    @classmethod
    def train(cls, pdf_model, t_x, t_y):
        batch_size = 64
        num_epochs = 50
        h_l = None
        h_vl = None
        s_x = t_x[np.random.randint(0, cls.test_set_size, 500)]
        s_y = t_y[np.random.randint(0, cls.test_set_size, 500)]
        for i in range(0, 5000):
            print('>>>>>')
            print('EPISODE: ' + str(i))
            history = model.fit(s_x,
                                s_y,
                                epochs=num_epochs,
                                batch_size=batch_size,
                                shuffle=True,
                                validation_split=0.15,
                                verbose=2
                                )
            hl = history.history['custom_loss1']
            hv = history.history['val_custom_loss1']
            if h_l is None:
                h_l = hl
                h_vl = hv
            else:
                h_l = h_l + hl
                h_vl = h_vl + hv
            print('<<<<<')

        cls.plot_results(h_l, h_vl, (num_epochs * (i + 1)))
        return


if __name__ == "__main__":
    pdf = PDFNeuralNet()
    model = pdf.build_pdf_model()
    x, y = pdf.generate_pdf_training_data()
    pdf.train(model, x, y)

    test = np.random.randint(PDFNeuralNet.test_set_size, size=20)
    _p = np.zeros((1, 9))
    for i in test:
        _p[0] = x[i]
        print('-----------------------')
        print('Yo: ' + str(y[i]))
        pr = model.predict(_p)
        print('Yp: ' + str(pr))
        print('1: ' + str(np.sum(pr)))
        print('Err: ' + str(y[i] - pr))
