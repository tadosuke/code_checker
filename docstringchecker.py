"""docstring と関数の引数・戻り値が一致しない箇所を検出するスクリプト."""

import ast
import re
import typing as tp

import sysargutil
from checkerbase import CheckerBase


class DocstringChecker(CheckerBase, ast.NodeVisitor):
    """docstring と関数の引数・戻り値が一致しない箇所を検出するクラス。

    :param file_path: チェック対象のファイルパス
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

    def check(self) -> None:
        """(override)チェックする."""
        print(f'[DocstringChecker] {self.file_path}')
        self.visit(self._tree)

    def visit_ClassDef(self, class_node: ast.ClassDef) -> None:
        """クラスノード用のビジター.

        :param class_node: クラスノード
        """
        self._check_class_docstrings(class_node)
        self.generic_visit(class_node)

    def visit_FunctionDef(self, func_node: ast.FunctionDef) -> None:
        """関数ノード用のビジター.

        :param func_node: 関数ノード
        """
        self._check_function_docstrings(func_node)
        self.generic_visit(func_node)

    def visit_AsyncFunctionDef(self, func_node: ast.AsyncFunctionDef) -> None:
        """async 関数ノード用のビジター.

        :param func_node: 関数ノード
        """
        self._check_function_docstrings(func_node)
        self.generic_visit(func_node)

    def _check_class_docstrings(self, class_node: ast.ClassDef) -> None:
        """クラスの docstring と __init__ 関数の引数をチェックする."""
        init_method = next((n for n in class_node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__'), None)
        if not init_method:
            return

        docstring = ast.get_docstring(class_node)
        if not docstring:
            return

        init_params = _AstNodeUtil._get_function_signature(init_method)
        doc_params = _parse_docstring(docstring)
        for param in init_params.keys():
            if param in ('return', 'self', 'cls'):
                continue
            if param not in doc_params:
                print(f"{class_node.name} クラスの __init__ で {param} が docstring にありません。({init_method.lineno} 行目)")

    def _check_function_docstrings(
            self,
            node: tp.Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> None:
        """関数の docstring と引数をチェック。"""
        docstring = ast.get_docstring(node)

        # 非公開関数はチェックしない
        if node.name.startswith('_'):
            return

        # init はクラスの docstring に含めるので、関数側ではチェックしない
        if node.name == '__init__':
            return

        # docstring の存在チェック
        if not docstring:
            print(f"{node.name} 関数に docstring がありません。({node.lineno} 行目)")
            return

        # パラメータの整合性チェック
        self._check_function_docstring_params(docstring, node)

    def _check_function_docstring_params(
            self,
            docstring: str,
            node: tp.Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> None:
        if _AstNodeUtil._is_property_node(node):
            # プロパティは型が明白なので、細かいチェックはしない
            return

        doc_params = _parse_docstring(docstring)
        func_params = _AstNodeUtil._get_function_signature(node)
        for param in func_params.keys():
            if param in ('self', 'cls', '*args', '**kwargs'):
                # 型ヒントがつけられないのでチェック不要
                continue
            if param == 'return' and _AstNodeUtil._is_return_none(node):
                # 戻り値がない場合はチェック不要
                continue

            if param not in doc_params:
                print(f"{node.name} 関数で {param} が docstring にありません。({node.lineno} 行目)")


class _AstNodeUtil:
    """ast.Node に関する便利関数."""

    @staticmethod
    def _is_return_none(node: ast.FunctionDef) -> bool:
        """戻り値が None か"""
        # 型ヒントがついていないと判別できない
        if node.returns is None:
            return False
        if not isinstance(node.returns, ast.NameConstant):
            return False

        return node.returns.value is None

    @staticmethod
    def _is_property_node(node: tp.Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
        """指定したノードがプロパティか？"""
        return any(isinstance(deco, ast.Name) and deco.id == 'property' for deco in node.decorator_list)

    @staticmethod
    def _get_function_signature(node: ast.FunctionDef) -> dict[str, str]:
        """関数のシグネチャを取得。"""
        signature = {}
        for arg in node.args.args:
            signature[arg.arg] = "param"
        if node.returns:
            signature["return"] = "return"
        return signature


def _parse_docstring(docstring: str) -> dict[str, str]:
    """docstring からパラメーターを抽出。"""
    lines = docstring.split("\n")
    params = {}
    for line in lines:
        # 引数
        match = re.search(r":param (\w+):", line)
        if match:
            param_name = match.group(1)
            params[param_name] = "param"

        # 戻り値
        match = re.search(r":return:", line)
        if match:
            params["return"] = "return"

    return params


def main():
    for file in sysargutil.get_str_list():
        DocstringChecker(file).check()


if __name__ == '__main__':
    main()
