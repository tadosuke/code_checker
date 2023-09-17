"""型ヒントの付け忘れを検出するスクリプト."""

import ast

from checkerbase import CheckerBase


class TypeHintChecker(CheckerBase):
    """型ヒントの付け忘れを検出するクラス.

    :param file_path: チェック対象のファイルパス
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def check(self) -> bool:
        """(override)チェックする."""
        print('[TypeHintChecker]')
        issues: list[str] = []
        for node in ast.walk(self._tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            self._check_argument_type_hints(node, issues)
            self._check_return_type_hints(node, issues)

        if issues:
            for issue in issues:
                print(issue)
            return False

        return True

    def _check_argument_type_hints(self, node: ast.FunctionDef, issues: list[str]) -> None:
        """引数の型ヒントをチェックする."""
        args = node.args
        for arg in args.args:
            if self._is_python_reserved_arg(arg.arg):
                continue
            if arg.annotation is None:
                issues.append(f"{node.name} 関数の引数 {arg.arg} に型ヒントがありません。({node.lineno} 行目)")

    def _check_return_type_hints(self, node: ast.FunctionDef, issues: list[str]) -> None:
        """戻り値の型ヒントをチェックする."""
        returns = node.returns
        if returns is None:
            issues.append(f"{node.name} 関数の戻り値に型ヒントがありません。({node.lineno} 行目)")

    def _is_python_reserved_arg(self, arg_name: str) -> bool:
        """引数名がPythonの予約語かどうかチェックする."""
        return arg_name == 'self' or arg_name == 'cls'


class FileFilter:
    """ファイルをフィルタリングするクラス."""

    @staticmethod
    def is_test_file(file_name: str) -> bool:
        """テスト用のファイルかどうかチェックする."""
        return file_name.startswith('test_')

    @staticmethod
    def is_python_file(file_name: str) -> bool:
        """Pythonファイルかどうかチェックする."""
        return file_name.endswith('.py')
