#!/usr/bin/env python3
from collections.abc import Callable
from io import BufferedReader, TextIOWrapper
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
    file_path: str | PathLike[str],
    *,
    mode: Literal['r', 'rb'] = 'r',
    encoding: str | None = 'utf-8',
) -> T:
    p = Path(file_path)

    if mode == 'rb':
        encoding = None

    try:
        with p.open(mode=mode, encoding=encoding) as f:
            f = cast('TextIOWrapper | BufferedReader', f)
            read_data: T = func(f)
    except UnicodeDecodeError:
        log.debug(f'読み込もうとしたファイルの文字コードがUTF-8ではありませんでした: {file_path}')
        guess_encoding = check_encoding_open_file(p)

        if guess_encoding is None:
            log.warning(
                'chardetによる文字コードの判定に失敗、読み込みできず'
                f'(return empty {type(return_empty_value)})'
            )
            return return_empty_value

        log.debug('文字コードを推定できたのでファイルを読み込みます')
        with p.open(mode='r', encoding=guess_encoding) as f:
            return func(f)
    except FileNotFoundError:
        log.warning(
            '読み込もうとしたファイルが存在しません'
            f'(return empty {type(return_empty_value)}): {file_path}'
        )
        return return_empty_value
    except PermissionError:
        log.warning(
            '読み込み権限がないか、ファイルへのパスが正しく指定されていません'
            f'(return empty {type(return_empty_value)}): {file_path}'
        )
        return return_empty_value
    except ParserError:
        log.exception(
            f'ファイルの記述が不正です(return empty {type(return_empty_value)}): {file_path}'
        )
        return return_empty_value
    else:
        return read_data
