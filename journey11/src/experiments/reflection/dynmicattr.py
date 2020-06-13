import re


class A:
    def __str__(self):
        hidden = re.compile("^__.*__$")
        s = str()
        for itm in dir(self):
            o = getattr(self, itm)
            if not callable(o) and hidden.search(itm) is None:
                s = "{} [{}:{}]".format(s, itm, str(o))
        return s

    pass


if __name__ == "__main__":
    # Quick test to add new member variables via setattr
    #
    a = A()
    setattr(a, "_var", 1)
    setattr(a, "_str", "A String")
    print(str(a))
