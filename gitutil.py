"""Git 関連の便利関数モジュール."""

import subprocess


def get_changed_file_fullpaths(repository_root_directory: str) -> list[str]:
    """変更されているファイルのフルパスのリストを得る.

    コミットしていないファイルのみが対象となります。

    :param repository_root_directory: リポジトリのルートディレクトリ
    :return: 変更されたファイルパス（フルパス）のリスト。エラー時は空リスト
    """
    if repository_root_directory == '':
        return []

    file_names = get_changed_file_names(repository_root_directory)
    if len(file_names) == 0:
        return []

    return [f'{repository_root_directory}/{file_name}' for file_name in file_names]


def get_changed_file_names(repository_root_directory: str) -> list[str]:
    """変更されているファイル名のリストを得る.

    コミットしていないファイルのみが対象となります。

    :param repository_root_directory: リポジトリのルートディレクトリ
    :return: 変更されたファイル名のリスト。エラー時は空リスト
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
            cwd=repository_root_directory)
    except Exception:
        return []
    return result.stdout.strip().split("\n")
