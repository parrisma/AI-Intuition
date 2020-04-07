from journey11.src.lib.uniqueref import UniqueRef


class UniqueTopic:

    @classmethod
    def topic(cls,
              prefix: str = None) -> str:
        """
        Generate a universally unique topic name
        :return: Universally unique topic name
        """
        if prefix is None:
            prefix = ''
            sep = ''
        else:
            sep = '.'
        return "{}{}{}".format(prefix, sep, UniqueRef().ref)

    def __str__(self):
        return self.topic()

    def __repr__(self):
        return str(self)
