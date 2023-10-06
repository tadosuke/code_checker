"""Python コードに対して様々なチェックを行うスクリプト."""

import os.path

from dictiterationchecker import DictIterationAstCodeChecker
from docstringchecker import DocstringAstCodeChecker
from reassignmentchecker import ReassignmentAstCodeChecker
import sysargutil
from typehintchecker import TypeHintAstCodeChecker
from patternchecker import PatternCodeChecker

# チェック項目
_CHECKER_CLASS_LIST = (
    ReassignmentAstCodeChecker,  # ローカル変数の再代入チェック
    DocstringAstCodeChecker,  # docstring の整合性チェック
    TypeHintAstCodeChecker,  # 型ヒントチェック
    DictIterationAstCodeChecker,  # 辞書イテレート中の不正操作チェック
    PatternCodeChecker,
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
