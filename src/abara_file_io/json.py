#!/usr/bin/env python3
import json
from logging import getLogger
from os import PathLike
from pathlib import Path

log = getLogger(__name__)


def read_json(path: str | PathLike) -> dict:
    """jsonファイルを読み込む

    Args:
        path (str): 読み込むjsonファイルのパス

    Returns:
        dict: 辞書
    """
    try:
        with Path(path).open(encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        log.warning(
            f'読み込もうとしたファイルが存在しませんでした {e}\n'
            f'read_json から empty dict が返されました'
        )
        return {}


def write_json(data: dict, path: str | PathLike, *, ensure_ascii: bool = False) -> None:
    r"""jsonファイルを書き込む

    Args:
        data (dict): jsonに書き込む辞書オブジェクト
        path (str): ファイルパス
        ensure_ascii (bool): 非ASCII文字をエスケープする('あ'→'\\u3042')
    """
    with Path(path).open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=ensure_ascii)
