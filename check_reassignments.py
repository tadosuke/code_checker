"""ローカル変数の再代入を行っている箇所を検出するスクリプト."""

import ast
import sys


class ReassignmentChecker:

    def __init__(self, file_path: str) -> None:
        self.tree = self._create_ast_tree(file_path)

    def check(self) -> None:
        """チェックする."""
        print('[ReassignmentChecker]')
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self._check_in_function(node)

    def _create_ast_tree(self, filename: str) -> ast.Module:
        """ファイルからASTを生成."""
        with open(filename, "r", encoding='utf-8') as f:
            return ast.parse(f.read())

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


def main() -> None:
    file_path = sys.argv[1]
    ReassignmentChecker(file_path).check()


if __name__ == "__main__":
    main()
