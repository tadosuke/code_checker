"""ローカル変数の再代入を行っている箇所を指摘してくれるスクリプト."""

import ast
import sys


def analyze_file(filepath: str) -> None:
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()

    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            _find_reassignments_in_function(node)


def _find_reassignments_in_function(node: ast.FunctionDef) -> None:
    variables = set()
    for stmt in node.body:
        if not isinstance(stmt, ast.Assign):
            continue
        for target in stmt.targets:
            if not isinstance(target, ast.Name):
                continue
            if target.id in variables:
                print(f"Note: Reassignment of local variable '{target.id}' at line {target.lineno}")
                continue
            variables.add(target.id)


def main() -> None:
    filepath = sys.argv[1]
    analyze_file(filepath)


if __name__ == "__main__":
    main()
