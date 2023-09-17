"""docstring と関数の引数・戻り値が一致しない箇所を検出するスクリプト."""

import ast
import re
import sys


class DocstringChecker:
    """Docstring のチェックを行うクラス。

    :param filename: チェックを行いたい Python ファイル名
    """

    def __init__(self, filename: str) -> None:
        self.tree = self._create_ast_tree(filename)

    def check(self) -> None:
        """メインのチェック関数。"""
        print('[DocstringChecker]')
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self._check_class_docstrings(node)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                self._check_function_docstrings(node)

    def _create_ast_tree(self, filename: str) -> ast.Module:
        """ファイルからASTを生成。"""
        with open(filename, "r", encoding='utf-8') as f:
            return ast.parse(f.read())

    def _check_class_docstrings(self, node: ast.ClassDef) -> None:
        """クラスのdocstringと__init__関数の引数をチェック。"""
        docstring = ast.get_docstring(node)
        if not docstring:
            return
        init_method = next((n for n in node.body if isinstance(n, ast.FunctionDef) and n.name == '__init__'), None)
        if not init_method:
            return
        init_params = self._get_function_signature(init_method)
        doc_params = self._parse_docstring(docstring)
        for param in init_params.keys():
            if param in ('return', 'self', 'cls'):
                continue
            if param not in doc_params:
                print(f"{node.name} クラスの __init__ で {param} がdocstringにありません。({init_method.lineno} 行目)")

    def _check_function_docstrings(self, node: ast.FunctionDef) -> None:
        """関数のdocstringと引数をチェック。"""
        if any(isinstance(deco, ast.Name) and deco.id == 'property' for deco in node.decorator_list):
            return
        docstring = ast.get_docstring(node)
        if not docstring:
            return
        doc_params = self._parse_docstring(docstring)
        func_params = self._get_function_signature(node)
        for param in func_params.keys():
            if param not in doc_params and param not in ('self', 'cls'):
                print(f"{node.name} 関数で {param} がdocstringにありません。({node.lineno} 行目)")

    def _parse_docstring(self, docstring: str) -> dict[str, str]:
        """docstringからパラメーターを抽出。"""
        lines = docstring.split("\n")
        params = {}
        for line in lines:
            match = re.search(r":param (\w+):", line)
            if match:
                param_name = match.group(1)
                params[param_name] = "param"
            match = re.search(r":return:", line)
            if match:
                params["return"] = "return"
        return params

    def _get_function_signature(self, node: ast.FunctionDef) -> dict[str, str]:
        """関数のシグネチャを取得。"""
        signature = {}
        for arg in node.args.args:
            signature[arg.arg] = "param"
        if node.returns:
            signature["return"] = "return"
        return signature


def main():
    filename = sys.argv[1]
    checker = DocstringChecker(filename)
    checker.check()


if __name__ == "__main__":
    main()