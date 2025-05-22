#!/usr/bin/env python3
from collections.abc import Callable
from io import BufferedReader, BufferedWriter, TextIOWrapper
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import Literal, TypeVar, cast

from ruamel.yaml.parser import ParserError

from abara_file_io.util import check_encoding_open_file

log = getLogger(__name__)

T = TypeVar('T')


def common_file_read_exception_handling(
    func: Callable[[TextIOWrapper | BufferedReader], T],
    return_empty_value: T,
    path: str | PathLike[str],
    *,
    mode: Literal['r', 'rb'] = 'r',
    encoding: str | None = 'utf-8',
) -> T:
    """ファイル読み込み時の汎用的な例外処理をするラッパー関数

    Args:
        func (Callable[[TextIOWrapper  |  BufferedReader], T]): _description_
        return_empty_value (T): _description_
        path (str | PathLike[str]): _description_
        mode (Literal[&#39;r&#39;, &#39;rb&#39;], optional): _description_. Defaults to 'r'.
        encoding (str | None, optional): _description_. Defaults to 'utf-8'.

    Returns:
        T: _description_
    """
    p = Path(path)

    if mode == 'rb':
        encoding = None

    try:
        with p.open(mode=mode, encoding=encoding) as f:
            f = cast('TextIOWrapper | BufferedReader', f)
            read_data: T = func(f)
    except UnicodeDecodeError:
        log.debug(f'読み込もうとしたファイルの文字コードがUTF-8ではありませんでした: {path}')
        guess_encoding = check_encoding_open_file(p)

        if isinstance(guess_encoding, str):
            log.debug('文字コードを推定できたのでファイルを読み込みます')
            with p.open(mode='r', encoding=guess_encoding) as f:
                return func(f)

        log.warning(
            'chardetによる文字コードの判定に失敗、読み込みできず'
            f'(return empty {type(return_empty_value)})'
        )
    except FileNotFoundError:
        log.warning(
            '読み込もうとしたファイルが存在しません'
            f'(return empty {type(return_empty_value)}): {path}'
        )
    except PermissionError:
        log.warning(
            '読み込み権限がないか、ファイルへのパスが正しく指定されていません'
            f'(return empty {type(return_empty_value)}): {path}'
        )
    except IsADirectoryError:
        log.warning(
            '読み込もうとしたパスがディレクトリを指しています'
            f'(return empty {type(return_empty_value)}): {path}'
        )
    except OSError:
        log.warning(f'OSで問題が発生しました(return empty {type(return_empty_value)}): {path}')
    except ParserError:
        log.warning(f'ファイルの記述が不正です(return empty {type(return_empty_value)}): {path}')
    else:
        return read_data

    return return_empty_value


def common_file_write_exception_handling(
    func: Callable[[TextIOWrapper | BufferedWriter, object], None],
    data: object,
    path: str | PathLike[str],
) -> None:
    """ファイル書き込み時の汎用的な例外処理をするラッパー関数

    Args:
        func (Callable[[TextIOWrapper  |  BufferedReader], T]): _description_
        data (T): _description_
        path (str | PathLike[str]): _description_
    """
    p = Path(path)

    p.parent.mkdir(parents=True, exist_ok=True)

    # batファイルとcmdファイル作成時はShift-JIS + \r\nにする例外処理
    shft_jis_crlf: bool = False
    if p.suffix in {'.bat', '.cmd'}:
        shft_jis_crlf = True

    try:
        if shft_jis_crlf is False:
            with Path(p).open(mode='w', encoding='utf_8', newline='\n') as f:
                func(f, data)
        else:
            with Path(p).open(mode='w', encoding='cp932', newline='\r\n') as f:
                func(f, data)
    except PermissionError:
        log.warning(f'書き込み権限がないか、ファイルへのパスが正しく指定されていません: {path}')
    except IsADirectoryError:
        log.warning(f'書き込もうとしたパスがディレクトリを指しています: {path}')
    except OSError:
        log.warning(f'OSで問題が発生しました: {path}')
