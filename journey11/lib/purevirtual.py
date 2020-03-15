"""
Decorator to throw exception for all abstract methods with no intended implementation
"""


def purevirtual(func):
    def wrapper():
        raise NotImplementedError(
            "{} is a pure virtual function and must be implemented by child class".format(func.__name__))

    return wrapper
