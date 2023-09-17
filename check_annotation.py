"""型ヒントの付け忘れを検出するスクリプト."""

import ast
import os
import subprocess
import sys


class TypeHintChecker:
    """型ヒントをチェックするクラス."""

    def check_type_hints_in_file(self, file_path: str) -> bool:
        """Pythonファイル内の型ヒントをチェックする."""
        tree = self._create_ast_tree(file_path)
        issues: list[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            self._check_argument_type_hints(node, issues)
            self._check_return_type_hints(node, issues)

        if issues:
            for issue in issues:
                sys.stderr.write(issue)
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
                issues.append(f"関数 '{node.name}' の引数 '{arg.arg}' に型ヒントがありません。\n")

    def _is_python_reserved_arg(self, arg_name: str) -> bool:
        """引数名がPythonの予約語かどうかチェックする."""
        return arg_name == 'self' or arg_name == 'cls'

    def _check_return_type_hints(self, node: ast.FunctionDef, issues: list[str]) -> None:
        """戻り値の型ヒントをチェックする."""
        returns = node.returns
        if returns is None:
            issues.append(f"関数 '{node.name}' の戻り値に型ヒントがありません。\n")


class FileFinder:
    """ファイルを探すクラス."""

    @staticmethod
    def get_files_from_git_diff() -> list[str]:
        """Gitのdiffからファイル名を取得する."""
        result = subprocess.run(["git", "diff", "--name-only", "HEAD", "HEAD~"], capture_output=True, text=True)
        return result.stdout.strip().split("\n")

    @staticmethod
    def get_files_from_argv() -> list[str]:
        """コマンドライン引数からファイル名を取得する."""
        return sys.argv[1:]


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
    target_files = FileFinder.get_files_from_argv()
    if not target_files:
        sys.stderr.write('対象ファイルが指定されていません')
        exit(1)

    root_folder = os.getcwd()
    type_checker = TypeHintChecker()
    for file in target_files:
        if not FileFilter.is_python_file(file):
            continue
        if FileFilter.is_test_file(file):
            continue

        full_file_path = os.path.join(root_folder, file)
        if not type_checker.check_type_hints_in_file(full_file_path):
            exit(1)


if __name__ == "__main__":
    main()
