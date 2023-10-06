
_PRIVATE_MODULE_CONSTANT = 0
PUBLIC_MODULE_CONSTANT = 0
_private_module_variable = 0
public_module_variable = 0


class MyClass:

    _PRIVATE_CLASS_CONSTANT = 0
    PUBLIC_CLASS_CONSTANT = 0
    _private_class_variable = 0
    public_class_variable = 0

    def __init__(self, number: int) -> None:
        self._a = number
        self._b = 0
        self.public = 0

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


def _dict_iteration() -> None:
    test_dict = {
        'a': 0,
        'b': 1,
        'c': 2,
    }

    for key, value in test_dict.items():
        if key == 'a':
            test_dict.pop(key)
            continue
        if key == 'b':
            del test_dict[key]
            continue


# unittest.skip()
