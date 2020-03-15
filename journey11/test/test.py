from abc import ABC, abstractmethod


def must_implement(*attrs):
    def class_rebuilder(cls):
        class NewClass(cls):
            def __init__(self):
                print("\nMust Implement Decorator Init")
                cl = getattr(self, "__call__", None)
                if not callable(cl):
                    raise NotImplementedError("Class must implement __call__(self, arg1)".format(""))
                super().__init__()

        return NewClass

    return class_rebuilder


class A(ABC):

    def __init__(self):
        print("\nA Init")
        # cl = getattr(self, "__call__", None)
        # if not callable(cl):
        #    raise NotImplementedError("Must implement __call__(self, arg1)")
        # return

    @abstractmethod
    def a(self):
        print("A call a()")


@must_implement("__call__")
class B(A):

    def __init__(self):
        super().__init__()
        print("B Init")

    def __call__(self, arg1):
        print("B.__call__")
        return

    def a(self):
        print("B call a()")


@must_implement("__call__")
class C(A):

    def __init__(self):
        super().__init__()
        print("C Init")

    def a(self):
        print("C call a()")


if __name__ == "__main__":
    b = B()
    b.a()

    try:
        c = C()
        AssertionError("NotImplementedError expected")
    except NotImplementedError:
        print("Expected exception Ok")
