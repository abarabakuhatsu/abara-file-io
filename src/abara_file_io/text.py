#!/usr/bin/env python3
from io import BufferedReader, BufferedWriter, TextIOWrapper
from logging import getLogger
from os import PathLike
from pathlib import Path

from abara_file_io.common_io_wrapper import (
    common_file_read_exception_handling,
    common_file_write_exception_handling,
)

log = getLogger(__name__)


def read_text(path: Path | str, *, encoding: str = 'utf-8') -> str:
    """テキスト形式のファイルをstrとして読み込む

    UTF-8以外のファイルはchardetで文字コードを自動判定する

    Args:
        path (Path | str): 開くファイルのパス
        encoding (str): 読み込むファイルエンコード形式（自動推測）

    Returns:
        str: 読み込んだ文字列、もしファイルが読み込めない場合は空文字列を返す
    """

    def read_text_core(f: TextIOWrapper | BufferedReader) -> str:
        if isinstance(f, TextIOWrapper):
            return f.read()
        return str(f.read())

    return common_file_read_exception_handling(
        func=read_text_core, return_empty_value='', path=path, encoding=encoding
    )


def write_text(data: str, path: str | PathLike[str]) -> None:
    r"""strデータをファイルを書き込む

    テキストファイルを標準的な UTF-8 + \n の形式で保存する
    ただし拡張子.batと.cmdを指定した場合のみ、例外として Shift-JIS + \r\n で保存する

    Args:
        data (str): 書き込む文字列
        path (str | PathLike[str]): 拡張子も含めて記述する
    """

    def write_text_core(
        f: TextIOWrapper | BufferedWriter,
        data: object,
    ) -> None:
        if isinstance(f, TextIOWrapper) and isinstance(data, str):
            f.write(data)

    common_file_write_exception_handling(func=write_text_core, data=data, path=path)
