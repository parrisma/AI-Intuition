from abc import ABC, abstractmethod


class JException(Exception):
    @abstractmethod
    def as_string(self,
                  as_feature: bool = False) -> str:
        """
        The exception rendered as string, if as_feature = True then as a feature vector equivalent for use in AL/ML
        context.
        :return: Exception as string
        """
        raise NotImplementedError
