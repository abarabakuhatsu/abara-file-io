#!/usr/bin/env python3
import tomllib
from logging import getLogger
from os import PathLike
from pathlib import Path

import tomli_w

log = getLogger(__name__)


def read_toml_file(file_path: str | PathLike) -> dict:
    """TOMLファイルを読み込む

        読み込みに失敗した場合は空の辞書を返す

    Args:
        file_path (Union[Path, str]): 読み込むファイルのパス

    Returns:
        Union[dict, None]:
            正確にはdictのインスタンスのruamel.yaml.comments.CommentedMap
    """
    try:
        path_obj = Path(file_path)

        with path_obj.open(mode='rb') as f:
            return tomllib.load(f)
    except FileNotFoundError as errorName:
        log.warning(
            f'読み込もうとしたファイルが存在しません [{errorName}]\n'
            'read_toml_file から empty dict が返されました'
        )
        return {}
    except PermissionError as errorName:
        log.warning(
            f'読み込みファイル名が正しく指定されていません [{errorName}]\n'
            f'read_toml_file から empty dict が返されました'
        )
        return {}


def write_toml_file(write_data: dict, file_path: str | PathLike) -> None:
    """TOMLとして書き込む

        第一引数で受け取ったパスに、第二引数で受け取った内容をTOMLとして書き込む。
        ※tomli_wが必要
        tomli_wでの書き込みはコメントが消えるので注意
        保持したい場合はtomlkitを使うこと

    Args:
        write_data (dict): 書き込むデータ
        file_path (str | PathLike): 書き込むファイルのパス
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    try:
        path_obj = Path(file_path)

        with path_obj.open(mode='wb') as toml_file:
            tomli_w.dump(write_data, toml_file)
    except PermissionError:
        log.exception(f'書き込もうとしたファイルの権限がありません [{file_path}]')
