#!/usr/bin/env python3
import json
from io import BufferedReader, TextIOWrapper
from logging import getLogger
from os import PathLike
from pathlib import Path

from abara_file_io.common_io_wrapper import common_file_read_exception_handling

log = getLogger(__name__)


def read_json(path: str | PathLike) -> dict:
    """jsonファイルを読み込む

    Args:
        path (str): 読み込むjsonファイルのパス

    Returns:
        dict: 辞書
    """

    def read_json_core(
        f: TextIOWrapper | BufferedReader,
    ) -> dict:
        if isinstance(f, TextIOWrapper):
            return json.load(f)
        return {}

    return common_file_read_exception_handling(
        func=read_json_core, return_empty_value={}, file_path=path
    )


def write_json(data: dict, path: str | PathLike, *, ensure_ascii: bool = False) -> None:
    r"""jsonファイルを書き込む

    Args:
        data (dict): jsonに書き込む辞書オブジェクト
        path (str): ファイルパス
        ensure_ascii (bool): 非ASCII文字をエスケープする('あ'→'\\u3042')
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with Path(path).open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=ensure_ascii)
