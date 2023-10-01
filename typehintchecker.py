"""型ヒントの付け忘れを検出するスクリプト."""

import ast
import typing as tp

import sysargutil
from checkerbase import CheckerBase


class TypeHintChecker(CheckerBase, ast.NodeVisitor):
    """型ヒントの付け忘れを検出するクラス.

    :param file_path: チェック対象のファイルパス
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.issues: list[str] = []

    def check(self) -> bool:
        """(override)チェックする."""
        print('[TypeHintChecker]')
        self.visit(self._tree)

        if self.issues:
            for issue in self.issues:
                print(issue)
            return False

        return True

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_argument_type_hints(node)
        self._check_return_type_hints(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_argument_type_hints(node)
        self._check_return_type_hints(node)
        self.generic_visit(node)

    def _check_argument_type_hints(
            self,
            node: tp.Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> None:
        """引数の型ヒントをチェックする."""
        args = node.args
        for arg in args.args:
            if _is_python_reserved_arg(arg.arg):
                continue
            if arg.annotation is None:
                self.issues.append(f"{node.name} 関数の引数 {arg.arg} に型ヒントがありません。({node.lineno} 行目)")

    def _check_return_type_hints(
            self,
            node: tp.Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> None:
        """戻り値の型ヒントをチェックする."""
        returns = node.returns
        if returns is None:
            if node.name == '__init__':
                self.issues.append(f"{node.name} の戻り値は None であるべきです。({node.lineno} 行目)")
            else:
                self.issues.append(f"{node.name} 関数の戻り値に型ヒントがありません。({node.lineno} 行目)")


def _is_python_reserved_arg(arg_name: str) -> bool:
    """引数名がPythonの予約語かどうかチェックする."""
    return arg_name == 'self' or arg_name == 'cls'


def main():
    for file in sysargutil.get_str_list():
        TypeHintChecker(file).check()


if __name__ == '__main__':
    main()
