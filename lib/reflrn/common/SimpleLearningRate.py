from lib.reflrn.interface.LearningRate import LearningRate


class SimpleLearningRate(LearningRate):
    """
    Implements the LearningRate abstract class interface so that it is compatible with reinforcement learning
    utilities reflrn

    Simple learning rate calc: lr = lr_zero / (1 + (step * lr_decay_factor))

    :param lr0 - Initial learning rate
    :param lrd - learning rate decay
    :param lr_min - the smallest value that can be returned for learning rate
    """

    def __init__(self,
                 lr0: float,
                 lrd: float,
                 lr_min: float = float(0)):
        self.__lr0 = lr0
        self.__lrd = lrd
        self.__lr_min = lr_min
        return

    def learning_rate(self,
                      step: int) -> float:
        """
        The learning rate for the given step
        :param step: The step to calculate the learning rate for
        :return: the learning rate
        """
        lr = self.__lr0 / (1 + (step * self.__lrd))
        return max(self.__lr_min, lr)

    #
    # What learning rate decay would give a learning_rate_target (value) after target_step steps ?
    #
    @classmethod
    def lr_decay_target(cls,
                        learning_rate_zero: float,
                        target_step: int,
                        target_learning_rate: float) -> float:
        """
        Reverse engineer a learning rate decay to hit a given learning rate after a given number of steps
        :param learning_rate_zero: The initial learning rate
        :param target_step: The step at which the learning rate would equal the target
        :param target_learning_rate: the target learning rate we are trying to hit
        :return:
        """
        if target_step <= 0:
            raise ValueError("Target Step must be >= 1")
        return (learning_rate_zero - target_learning_rate) / (target_step * target_learning_rate)
