"""ローカル変数の再代入を行っている箇所を検出するスクリプト."""

import ast

import sysargutil
from checkerbase import CheckerBase


class ReassignmentChecker(CheckerBase, ast.NodeVisitor):
    """ローカル変数の再代入を行っている箇所を検出するクラス。

    :param file_path: チェック対象のファイルパス
    """

    def __init__(
            self,
            file_path: str) -> None:
        super().__init__(file_path)

    def check(self) -> None:
        """(override)チェックする."""
        print(f'[ローカル変数の再代入チェック] {self.file_path}')
        self.visit(self._tree)

    def visit_FunctionDef(
            self,
            node: ast.FunctionDef) -> None:
        """(override)関数を訪れたときに呼ばれる."""
        self._check_in_function(node)
        self.generic_visit(node)  # 子の visit が呼ばれるために必要

    def _check_in_function(
            self,
            func_node: ast.FunctionDef) -> None:
        """関数内のローカル変数が再代入されていないかチェックする。"""
        assigned_variables: set[str] = set()
        for stmt in func_node.body:
            self._check_statement_for_reassignment(stmt, assigned_variables)

    def _check_statement_for_reassignment(
            self,
            stmt: ast.stmt,
            assigned_variables: set[str]) -> None:
        """ステートメント内のローカル変数が再代入されていないかチェックする。"""
        self.visit(stmt)  # 再帰的にノードを訪問

        if not isinstance(stmt, ast.Assign):
            return

        self._check_assign_targets_for_reassignment(stmt.targets, assigned_variables)

    def _check_assign_targets_for_reassignment(
            self,
            targets: list[ast.expr],
            assigned_variables: set[str]) -> None:
        """代入の対象がローカル変数で、それが再代入されていないかチェックする。"""
        for target in targets:
            if not isinstance(target, ast.Name):
                continue

            variable_name = target.id
            if variable_name in assigned_variables:
                print(f"ローカル変数 '{variable_name}' は再代入されています。（{target.lineno} 行目）")
                continue

            assigned_variables.add(variable_name)


def main():
    for file in sysargutil.get_str_list():
        ReassignmentChecker(file).check()


if __name__ == '__main__':
    main()
