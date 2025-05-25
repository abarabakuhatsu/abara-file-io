#!/usr/bin/env python3
from logging import getLogger
from os import PathLike
from pathlib import Path

from chardet import UniversalDetector

log = getLogger(__name__)


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

    necessary_confidence: float = 0.8

    if encoding_info['encoding'] is None:
        log.error(f'文字コードが判別できませんでした {file_path}')
        return None

    if (
        encoding_info['encoding'].lower() == 'WINDOWS-1252'.lower()
        and encoding_info['confidence'] <= necessary_confidence
    ):
        log.debug(
            'サンプル文字数が足りずにShift-JISをWINDOWS-1252に誤検出した可能性が高いので、Windows標準の拡張SHIFT_JISであるcp932(Windows-31J)として処理'
        )
        return 'cp932'

    if encoding_info['encoding'].lower() == 'SHIFT_JIS'.lower():
        log.debug(
            'SHIFT_JIS(JIS X0208-1997)はWindows標準の拡張SHIFT_JISである'
            'CP932(Windows-31J)として処理'
        )
        return 'cp932'

    return encoding_info['encoding']
