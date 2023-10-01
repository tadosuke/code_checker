"""コードチェッククラスの共通機能を提供するモジュール."""

from abc import abstractmethod
import ast


class CheckerBase:
    """コードチェックの基底クラス.

    :param file_path: チェック対象のファイルパス
    """

    def __init__(self, file_path: str) -> None:
        self._filepath = file_path
        self._tree = self._create_ast_tree(file_path)

    @property
    def file_path(self) -> str:
        """ファイルパス."""
        return self._filepath

    @property
    def tree(self) -> ast.AST:
        """抽象構文木."""
        return self._tree

    @abstractmethod
    def check(self) -> None:
        """チェックする."""
        pass

    def _create_ast_tree(self, file_path: str) -> ast.AST:
        """抽象構文木（AST）を生成する."""
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        return tree
