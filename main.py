"""Python コードに対して様々なチェックを行うスクリプト."""

import os.path

import sysargutil
from docstringchecker import DocstringChecker
from reassignmentchecker import ReassignmentChecker
from typehintchecker import TypeHintChecker
from unusedprivatevariablechecker import UnusedPrivateVariableChecker
from dictiterationchecker import DictIterationChecker


# チェック項目
_CHECKER_CLASS_LIST = (
    ReassignmentChecker,  # ローカル変数の再代入チェック
    DocstringChecker,  # docstring の整合性チェック
    TypeHintChecker,  # 型ヒントチェック
    UnusedPrivateVariableChecker,  # 未使用の非公開変数チェック
    DictIterationChecker,  # 辞書イテレート中の不正操作チェック
)


def main() -> None:
    for file_path in sysargutil.get_str_list():
        if not os.path.exists(file_path):
            print(f'ファイルが見つかりません（{file_path=}）')
            continue
        _check(file_path)


def _check(file_path):
    for checker_class in _CHECKER_CLASS_LIST:
        checker_class(file_path).check()
        print('')


if __name__ == "__main__":
    main()