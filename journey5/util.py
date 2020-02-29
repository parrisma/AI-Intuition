import numbers


class Util:
    @classmethod
    def to_pct(cls, x, y) -> str:
        """
        x as % of Y
        :param x: Value of x
        :param y: Value oy y
        :return: X as % of Y as str
        """
        if not isinstance(x, numbers.Number) or not isinstance(x, numbers.Number):
            raise ValueError("All arguments must be numeric")
        return str(int((x / y) * 100))
