#!/usr/bin/env python3
from io import BufferedReader, TextIOWrapper
from logging import getLogger
from pathlib import Path

from abara_file_io.util import (
    common_file_read_exception_handling,
    create_file,
)

log = getLogger(__name__)


def read_str_file(file_path: Path | str, *, encoding: str = 'utf-8') -> str:
    """第一引数で受け取ったパスのファイルを文字列として読み込む

    Args:
        file_path (Path | str): 開くファイルのパス
        encoding (str): 読み込むファイルエンコード形式（自動推測）

    Returns:
        str: 読み込んだ文字列、もしファイルが読み込めない場合は空文字列を返す
    """

    def read_text(read_text: TextIOWrapper | BufferedReader) -> str:
        if isinstance(read_text, TextIOWrapper):
            return read_text.read()
        return str(read_text.read())

    return common_file_read_exception_handling(
        func=read_text, return_empty_value='', file_path=file_path, encoding=encoding
    )


def write_str_file(
    data: str,
    file_path: Path | str,
    *,
    crlf_preservation: bool = False,
) -> None:
    r"""第一引数で受け取った内容を、第二引数で受け取ったファイルに書き込む

    Args:
        data (str): 書き込むデータ
        file_path (Path | str): 書き込むファイルのパス
        crlf_preservation (bool, optional):
            改行コードを\nに修正せずデフォルトを保持する. Defaults to False.
    """
    p: Path = Path(file_path)

    try:
        create_file(p)
        if crlf_preservation is False:
            with Path(p).open(mode='w', encoding='utf-8', newline='\n') as t:
                t.write(data)
        else:
            p.write_text(data, encoding='utf-8')
    except PermissionError:
        log.exception(f'書き込みファイル名が正しく指定されていません [{file_path}]')
