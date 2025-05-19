#!/usr/bin/env python3
from logging import getLogger
from pathlib import Path

from .util import check_encoding_open_file, create_file

log = getLogger(__name__)


def read_str_file(file_path: Path | str, *, encoding: str = 'utf-8') -> str:
    """第一引数で受け取ったパスのファイルを文字列として読み込む

    Args:
        file_path (Path | str): 開くファイルのパス
        encoding (str): 読み込むファイルエンコード形式（自動推測）

    Returns:
        str: 読み込んだ文字列、もしファイルが読み込めない場合は空文字列を返す
    """
    p: Path = Path(file_path)

    try:
        f: str = p.read_text(encoding=encoding)
    except UnicodeDecodeError:
        log.debug(f'読み込もうとしたファイルの文字コードがUTF-8ではありませんでした: {file_path}')
        file_encoding = check_encoding_open_file(p)

        if file_encoding is None:
            log.warning('chardetによる文字コードの判定に失敗、読み込みできず(return empty str)')
            return ''

        log.debug('文字コードを推定できたのでファイルを読み込みます')
        return p.read_text(encoding=file_encoding)
    except FileNotFoundError:
        log.warning(f'読み込もうとしたファイルが存在しません(return empty str): {file_path}')
        return ''
    except PermissionError:
        log.warning(f'読み込みファイル名が正しく指定されていません(return empty str): {file_path}')
        return ''
    else:
        return f


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
