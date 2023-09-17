
class MyClass:

    def __init__(self, name):
        self._a = 0
        pass

    @property
    def a(self):
        """プロパティ."""
        return self._a


def func_a(name):
    """関数A.

    :param number: 数字
    """
    x = 1
    x = 2
