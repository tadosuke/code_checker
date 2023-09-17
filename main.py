"""Python コードに対して様々なチェックを行うスクリプト."""

import os.path
import sys

from docstringchecker import DocstringChecker
from reassignmentchecker import ReassignmentChecker
from typehintchecker import TypeHintChecker


# チェック項目
_CHECKER_CLASS_LIST = (
    ReassignmentChecker,  # ローカル変数の再代入チェック
    DocstringChecker,  # docstring の整合性チェック
    TypeHintChecker,  # 型ヒントチェック
)


def main() -> None:
    if len(sys.argv) != 2:
        print('引数の数が不正です.')
        return

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f'ファイルが見つかりません（{file_path=}）')
        return

    for checker_class in _CHECKER_CLASS_LIST:
        checker_class(file_path).check()
        print('')


if __name__ == "__main__":
    main()