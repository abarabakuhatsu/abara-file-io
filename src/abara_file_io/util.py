#!/usr/bin/env python3
from logging import getLogger
from os import PathLike
from pathlib import Path

from chardet import UniversalDetector

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


if __name__ == '__main__':
    pass
