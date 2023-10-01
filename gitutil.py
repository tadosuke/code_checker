"""Git 関連の便利関数モジュール."""

import subprocess


def get_changed_file_fullpaths() -> list[str]:
    """変更されているファイルのフルパスのリストを得る.

    :return: ファイルパス（フルパス）のリスト。エラー時は空リスト
    """
    root_dir = get_root_directory()
    if root_dir == '':
        return []

    file_names = get_changed_file_names()
    if len(file_names) == 0:
        return []

    return [f'{root_dir}/{file_name}' for file_name in file_names]


def get_changed_file_names() -> list[str]:
    """変更されているファイル名のリストを得る.

    :return: ファイル名のリスト。エラー時は空リスト
    """
    try:
        result = subprocess.run(["git", "diff", "--name-only", "HEAD", "HEAD~"], capture_output=True, text=True)
    except Exception:
        return []
    return result.stdout.strip().split("\n")


def get_root_directory() -> str:
    """Git リポジトリのルートディレクトリを取得します.

    :return: ルートディレクトリ。エラー時は空文字列
    """
    try:
        root_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    except Exception:
        return ""
    return root_dir

