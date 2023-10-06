"""コードチェックの共通機能を提供するモジュール."""

from abc import abstractmethod


class CodeCheckerBase:
    """コードチェックの基底クラス.

    :param file_path: チェック対象のファイルパス
    """

    def __init__(self, file_path: str) -> None:
        self._filepath = file_path

    @property
    def file_path(self) -> str:
        """ファイルパス."""
        return self._filepath

    @abstractmethod
    def check(self) -> None:
        """チェックする."""
        pass
