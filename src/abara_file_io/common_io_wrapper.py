#!/usr/bin/env python3
from collections.abc import Callable
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import IO, Any, Literal

from ruamel.yaml.parser import ParserError

from abara_file_io.util import check_encoding_open_file

log = getLogger(__name__)


def common_file_read_exception_handling[T](
    func: Callable[[IO[Any]], T],
    return_empty_value: T,
    path: str | PathLike[str],
    *,
    mode: Literal['r', 'rb'] = 'r',
) -> T:
    """ファイル読み込み時の汎用的な例外処理をするラッパー関数

    Args:
        func (Callable[[IO[Any]], T]): openしたファイルの読み込みをする関数
        return_empty_value (T): 読み込み処理の失敗時に戻る値。これによって戻り値の型も決定する
        path (str | PathLike[str]): 開くファイルのパス
        mode (Literal['r', 'rb';], optional): 読み込むファイルを開く時のmode. Defaults to 'r'.

    Returns:
        T: _description_
    """
    p = Path(path)

    encoding = 'utf_8'
    if mode == 'rb':
        encoding = None

    try:
        with p.open(mode=mode, encoding=encoding) as f:
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
    func: Callable[[object, IO[Any]], None],
    data: object,
    path: str | PathLike[str],
    *,
    mode: Literal['w', 'wb'] = 'w',
) -> None:
    """ファイル書き込み時の汎用的な例外処理をするラッパー関数

    Args:
        func (Callable[[TextIOWrapper  |  BufferedReader], T]):
            openしたファイルに対して書き込み処理をする関数
        data (T): 書き込むデータ
        path (str | PathLike[str]): 保存するファイルのパス
        mode (Literal['w', 'wb'], optional): 書き込むファイルをopenする時のmode. Defaults to 'r'.
    """
    p = Path(path)

    encoding = 'utf_8'
    newline = '\n'
    if p.suffix in {'.bat', '.cmd'}:
        encoding = 'cp932'
        newline = '\r\n'
    if mode == 'wb':
        encoding = None
        newline = None

    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        with Path(p).open(mode=mode, encoding=encoding, newline=newline) as f:
            func(data, f)

    except PermissionError:
        log.warning(f'書き込み権限がないか、ファイルへのパスが正しく指定されていません: {path}')
    except IsADirectoryError:
        log.warning(f'書き込もうとしたパスがディレクトリを指しています: {path}')
    except OSError:
        log.warning(f'OSで問題が発生しました: {path}')
