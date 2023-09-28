"""モジュール内の未使用定数・変数を検出するスクリプト."""

import ast
import os
import sys

from checkerbase import CheckerBase


class UnusedPrivateVariableChecker(CheckerBase, ast.NodeVisitor):
    """未使用の非公開定数・変数を検出するクラス

    :param file_path: チェック対象のファイルパス
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._defined_vars = set()
        self._used_vars = set()

    def check(self) -> None:
        """(override)チェックする"""
        print('[未使用の非公開変数・定数]')
        self.visit(self._tree)
        results = self._defined_vars - self._used_vars
        if results:
            print("以下の非公開変数・定数はモジュール内で使用されていません")
            for r in results:
                print(f' {r}')

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.startswith('_'):
                self._defined_vars.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load) and node.id.startswith('_'):
            self._used_vars.add(node.id)
        self.generic_visit(node)


def main():
    if len(sys.argv) != 2:
        print('引数の数が不正です.')
        return

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f'ファイルが見つかりません（{file_path=}）')
        return

    UnusedPrivateVariableChecker(file_path).check()


if __name__ == '__main__':
    main()