"""辞書のイテレート中に禁止されている操作を行っている箇所を検出するモジュール.

「RuntimeError: dictionary changed size during」を未然に防ぐことを目的とします。
"""

import ast

import sysargutil
from checkerbase import CheckerBase


class DictIterationChecker(CheckerBase, ast.NodeVisitor):
    """辞書のイテレート中に禁止されている操作を行っている箇所を検出するクラス.

    :param file_path: チェック対象のファイルパス
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def check(self) -> None:
        print(f'[辞書イテレート中の削除操作] {self.file_path}')
        self.visit(self.tree)

    def visit_For(self, node: ast.For) -> None:
        self._check_dict_modify(node)
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self._check_dict_modify(node)
        self.generic_visit(node)

    def _check_dict_modify(self, node: ast.AST) -> None:
        for n in ast.walk(node):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                if n.func.attr == 'pop':
                    print(f'イテレート中に pop が呼ばれています。({n.lineno} 行目)')
            elif isinstance(n, ast.Delete):
                for target in n.targets:
                    if isinstance(target, ast.Subscript):
                        print(f'イテレート中に del が呼ばれています。({n.lineno} 行目)')


def main():
    for file in sysargutil.get_str_list():
        DictIterationChecker(file).check()


if __name__ == '__main__':
    main()