#!/usr/bin/env python3
from collections.abc import Callable
from io import BufferedReader, TextIOWrapper
from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import Literal, TypeVar, cast

from chardet import UniversalDetector
from ruamel.yaml.parser import ParserError

log = getLogger(__name__)


def create_file(file_path: Path) -> None:
    """ファイルの存在を確認し、存在しなければ作成する

    Args:
        file_path (Path): ファイルのパスオブジェクト
    """
    if file_path.exists():
        return

    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True)

    file_path.touch()
    return


def chack_file_exist(file_path: Path | str) -> bool:
    """ファイルの存在確認

    Args:
        file_path (Union[Path, str]): 確認するファイルのパス

    Returns:
        bool: ファイルが存在し、かつ中身があればTrue
    """
    p: Path = Path(file_path)

    file_exists = p.exists()

    if file_exists and p.stat().st_size > 0:
        log.debug(f'ファイル存在確認 : {file_path}')
        return True
    if file_exists:
        log.debug(f'中身のない空のファイルです : {file_path}')
        return False
    log.debug(f'ファイルは存在しません : {file_path}')
    return False


def check_encoding_open_file(file_path: PathLike | str) -> str | None:
    """ファイルを開いてchardetでエンコードを判定する

    Args:
        file_path (Union[PathLike, str]): 判定する文字列のパス

    Returns:
        Optional[str]: 判定したエンコーディング
    """
    log.debug('cardetによるエンコード判定を実行')

    detector = UniversalDetector()

    try:
        with Path(file_path).open(mode='rb') as f:
            while True:
                binary = f.readline()
                if binary == b'':
                    break  # ファイルの最後まで判定
                detector.feed(binary)
                if detector.done:
                    break  # confidenceが規定値以上
    finally:
        detector.close()

    encoding_info = detector.result
    log.debug(encoding_info)

    necessary_confidence: float = 0.5

    if (
        encoding_info['encoding'] == 'WINDOWS-1252'
        and encoding_info['confidence'] <= necessary_confidence
    ):
        log.debug(
            'サンプル文字数が足りずにWINDOWS-1252に誤検出した可能性が高いのでcp932(Windows-31J)として処理'
        )
        return 'cp932'
    if encoding_info['encoding'] == 'SHIFT_JIS':
        log.debug(
            'SHIFT_JIS(JIS X0208-1997)はWindows拡張SHIFT_JISであるCP932(Windows-31J)として処理'
        )
        return 'cp932'
    if encoding_info['encoding']:
        return encoding_info['encoding']
    log.error(f'文字コードが判別できませんでした {file_path}')
    return None


T = TypeVar('T')


def common_file_read_exception_handling(
    func: Callable[[TextIOWrapper | BufferedReader], T],
    return_empty_value: T,
    file_path: str | PathLike[str],
    *,
    mode: Literal['r', 'rb'] = 'r',
    encoding: str = 'utf-8',
) -> T:
    p = Path(file_path)
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
