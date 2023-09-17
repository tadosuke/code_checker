"""型ヒントの付け忘れを検出するスクリプト."""

import ast
import sys


class TypeHintChecker:
    """型ヒントをチェックするクラス."""

    def __init__(self, file_path: str) -> None:
        self.tree = self._create_ast_tree(file_path)

    def check(self) -> bool:
        """チェックする."""
        print('[TypeHintChecker]')
        issues: list[str] = []
        for node in ast.walk(self.tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            self._check_argument_type_hints(node, issues)
            self._check_return_type_hints(node, issues)

        if issues:
            for issue in issues:
                print(issue)
            return False

        return True

    def _create_ast_tree(self, file_path: str) -> ast.AST:
        """抽象構文木（AST）を生成する."""
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        return tree

    def _check_argument_type_hints(self, node: ast.FunctionDef, issues: list[str]) -> None:
        """引数の型ヒントをチェックする."""
        args = node.args
        for arg in args.args:
            if self._is_python_reserved_arg(arg.arg):
                continue
            if arg.annotation is None:
                issues.append(f"関数 '{node.name}' の引数 '{arg.arg}' に型ヒントがありません。({node.lineno} 行目)")

    def _check_return_type_hints(self, node: ast.FunctionDef, issues: list[str]) -> None:
        """戻り値の型ヒントをチェックする."""
        returns = node.returns
        if returns is None:
            issues.append(f"関数 '{node.name}' の戻り値に型ヒントがありません。({node.lineno} 行目)")

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


def main() -> None:
    """メイン関数."""
    if len(sys.argv) != 2:
        return

    file_path = sys.argv[1]
    if not file_path:
        return

    if not FileFilter.is_python_file(file_path):
        return
    if FileFilter.is_test_file(file_path):
        return

    TypeHintChecker(file_path).check()


if __name__ == "__main__":
    main()
