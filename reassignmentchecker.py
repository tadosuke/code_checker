"""ローカル変数の再代入を行っている箇所を検出するスクリプト."""

import ast

from checkerbase import CheckerBase


class ReassignmentChecker(CheckerBase):

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def check(self) -> None:
        """(override)チェックする."""
        print('[ReassignmentChecker]')
        for node in ast.walk(self._tree):
            if isinstance(node, ast.FunctionDef):
                self._check_in_function(node)

    def _check_in_function(self, func_node: ast.FunctionDef) -> None:
        """関数内をチェックする."""
        variables: set[str] = set()
        for stmt in func_node.body:
            if not isinstance(stmt, ast.Assign):
                continue
            for target in stmt.targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id in variables:
                    print(f"ローカル変数 '{target.id}' は再代入されています。（{target.lineno} 行目）")
                    continue
                variables.add(target.id)
