"""起動引数を解析するモジュール."""

import sys


def get_str_list() -> list[str]:
    """引数から文字列のリストを得ます.

    :return: 文字列のリスト
    """
    if len(sys.argv) < 2:
        print('引数が指定されていません。')
        return []

    return sys.argv[1:]
