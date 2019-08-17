import logging
import unittest

import numpy as np
import keras.backend as K
from keras.initializers import RandomUniform
from keras.initializers import Zeros
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils import multi_gpu_model
from lib.reflrn.interface.State import State


class PDFNeuralNet:
    def __init__(self):
        self.seed = 42.0
        self.state_size = 1
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
        bi = Zeros()

        pdf_model = Sequential()
        pdf_model.add(
            Dense(1600, input_dim=self.state_size, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        pdf_model.add(Dropout(0.1))
        pdf_model.add(Dense(800, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        pdf_model.add(Dropout(0.1))
        pdf_model.add(Dense(400, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        pdf_model.add(Dropout(0.05))
        pdf_model.add(Dense(100, activation='relu', kernel_initializer=ki, bias_initializer=bi))
        pdf_model.add(Dropout(0.05))

## ToDo re write with 2 outputs

        pdf_model.add(Dense(units=self.action_size, activation='linear', kernel_initializer=ki, bias_initializer=bi))
        if self.num_gpu > 0:
            pdf_model = multi_gpu_model(pdf_model, gpus=self.num_gpu)

        def mse_loss(y_true, y_pred):
            return K.sum(K.mean(K.square(y_pred - y_true), axis=-1))

        def sum1_loss(y_true, y_pred):
            return K.abs(1 - K.sum(y_pred))

        pdf_model.compile(loss=[mse_loss, sum1_loss],
                          optimizer=Adam(lr=self.learning_rate),
                          metrics=['mse']
                          )
        return pdf_model

    @classmethod
    def generate_pdf_training_data(cls):
        _x = np.zeros((100, 1))
        _y = np.zeros((100, 9))
        for i in range(0, 100):
            _pdf = np.random.randint(100, size=9)
            _pdf = _pdf / np.sum(_pdf)
            _x[i] = i
            _y[i] = _pdf
        return _x, _y

    @classmethod
    def train(cls, pdf_model, x, y):
        batch_size = 16
        num_epochs = 500
        history = model.fit(x, y,
                            epochs=num_epochs,
                            batch_size=batch_size,
                            shuffle=True,
                            )
        return


if __name__ == "__main__":
    pdf = PDFNeuralNet()
    model = pdf.build_pdf_model()
    x, y = pdf.generate_pdf_training_data()
    pdf.train(model, x, y)

    test = np.random.randint(100, size=20)
    _p = np.zeros((1, 1))
    for i in test:
        _p[0] = i
        print('-----------------------')
        print(str(y[i]))
        pr = model.predict(_p)
        print(str(pr))
        print(str(np.sum(pr)))
        print(str(y[i] - pr))
