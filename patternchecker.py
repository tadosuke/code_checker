"""コード内の特定のパターンを検出するモジュール."""

from codecheckerbase import CodeCheckerBase
import sysargutil


# 検出するパターン（検出する文字列、検出時のメッセージ）
_PATTERNS: dict[str, str] = {
    '# unittest.skip': 'unittest.skip のコメントアウトを戻し忘れていませんか？',
}


class PatternCodeChecker(CodeCheckerBase):
    """コード内の特定のパターンを検出するクラス."""

    def check(self) -> None:
        print(f'[特定パターンの検出] {self.file_path}')
        lines = self._read_file()
        for i, line in enumerate(lines):
            self._check_patterns(line, i)

    def _read_file(self) -> list[str]:
        """ファイルの内容を行ごとに読み込んで返すメソッド"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.readlines()

    def _check_patterns(self, line: str, line_number: int):
        for pattern, message in _PATTERNS.items():
            if pattern in line:
                print(f'{message} ({line_number} 行目)')


def main():
    for file in sysargutil.get_str_list():
        PatternCodeChecker(file).check()


if __name__ == '__main__':
    main()