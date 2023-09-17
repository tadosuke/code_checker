
class MyClass:

    def __init__(self, number: int) -> None:
        self._a = number

    @property
    def a(self) -> int:
        """プロパティ."""
        return self._a


def func_a(name):
    """関数A.

    :param number: 数字
    """
    x = 1
    y = name
    x = 2


def _func_b(name: str) -> None:
    pass
