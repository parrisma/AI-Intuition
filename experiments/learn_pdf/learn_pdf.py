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
    def __init__(self):
        self.seed = 42.0
        self.state_size = 9
        self.action_size = 9
        self.num_gpu = 2
        self.learning_rate = 0.001

    def build_pdf_model(self):
        """
        Simple fully connected network to learn the probability distribution over the action space where the
        most profitable action as defined by the critic will have the highest probability.

        :return: a Keras model capable of learning the probability distribution of a state space of approx 10K with
        and action space of 5 - 10
        """
        ki = RandomUniform(minval=-0.05, maxval=0.05, seed=self.seed)
        bi = RandomUniform(minval=-0.05, maxval=0.05, seed=self.seed) # Zeros()

        pdf_in = Input(shape=(self.state_size,), name="pdf_in")
        pdf_l1 = Dense(1600, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_in)
        pdf_l2 = Dropout(0.1)(pdf_l1)
        pdf_l3 = Dense(800, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l2)
        pdf_l4 = BatchNormalization()(pdf_l3)
        pdf_l5 = Dense(400, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l4)
        pdf_l6 = Dropout(0.05)(pdf_l5)
        pdf_l7 = Dense(100, activation='relu', kernel_initializer=ki, bias_initializer=bi)(pdf_l6)
        pdf_l8 = BatchNormalization()(pdf_l7)
        pdf_out = Dense(units=self.action_size, activation='linear')(
            pdf_l8)

        pdf_model = Model(inputs=[pdf_in], outputs=[pdf_out])

        if self.num_gpu > 0:
            pdf_model = multi_gpu_model(pdf_model, gpus=self.num_gpu)

        def custom_loss1(y_true, y_pred):
            mse = K.mean(K.square(y_true - y_pred), axis=-1)
            sum_constraint = K.abs(K.sum(y_pred, axis=-1) - 1)
            return mse + sum_constraint

        pdf_model.compile(loss=custom_loss1,
                          optimizer=Adam(),
                          metrics=[custom_loss1]
                          )

        print(pdf_model.summary())

        return pdf_model

    @classmethod
    def plot_results(cls,
                     history,
                     loss_name,
                     num_epochs):
        color_r = 'tab:red'
        color_b = 'tab:blue'

        epocs = np.arange(0, num_epochs)

        fig, _ = plt.subplots(figsize=(15, 6))

        # Loss
        ax1 = plt.subplot(1, 1, 1)
        plt.title('Loss')
        ax1.set_xlabel('Epoc')
        ax1.set_ylabel('Traing Loss', color=color_r)
        ax1.plot(epocs, history.history[loss_name], color=color_r)
        ax1.tick_params(axis='y', labelcolor=color_r)
        ax2 = ax1.twinx()  # 2nd Axis for Validation Loss
        ax2.set_ylabel('Validation Loss', color=color_b)
        ax2.plot(epocs, history.history['val_' + loss_name], color=color_b)
        ax2.tick_params(axis='y', labelcolor=color_b)

        # Accuracy
        # ax1 = plt.subplot(1, 2, 2)
        # plt.title('Accuracy')
        # ax1.set_xlabel('Epoc')
        # ax1.set_ylabel('Traing accuracy', color=color_r)
        # ax1.plot(epocs, history.history['acc'], color=color_r)
        # ax1.tick_params(axis='y', labelcolor=color_r)
        # ax2 = ax1.twinx()  # 2nd Axis for Validation Loss
        # ax2.set_ylabel('Validation Accuracy', color=color_b)
        # ax2.plot(epocs, history.history['val_acc'], color=color_b)
        # ax2.tick_params(axis='y', labelcolor=color_b)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()
        return

    @classmethod
    def generate_pdf_training_data(cls):
        _x = np.zeros((100, 9))
        _y = np.zeros((100, 9))
        u = dict()
        for i in range(0, 100):
            _pdf = np.random.randint(100, size=9)
            _pdf = _pdf / np.sum(_pdf)
            _x[i] = np.random.randint(2, size=9)
            _y[i] = _pdf
        return _x, _y

    @classmethod
    def train(cls, pdf_model, t_x, t_y):
        batch_size = 32
        num_epochs = 10000
        history = model.fit(t_x,
                            t_y,
                            epochs=num_epochs,
                            batch_size=batch_size,
                            shuffle=True,
                            validation_split=0.15,
                            verbose=2
                            )
        cls.plot_results(history, 'custom_loss1', num_epochs)
        return


if __name__ == "__main__":
    pdf = PDFNeuralNet()
    model = pdf.build_pdf_model()
    x, y = pdf.generate_pdf_training_data()
    pdf.train(model, x, y)

    test = np.random.randint(100, size=20)
    _p = np.zeros((1, 9))
    for i in test:
        _p[0] = x[i]
        print('-----------------------')
        print('Yo: ' + str(y[i]))
        pr = model.predict(_p)
        print('Yp: ' + str(pr))
        print('1: ' + str(np.sum(pr)))
        print('Err: ' + str(y[i] - pr))
