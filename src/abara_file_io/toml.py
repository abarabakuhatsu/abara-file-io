#!/usr/bin/env python3
import tomllib
from io import BufferedReader, TextIOWrapper
from logging import getLogger
from os import PathLike
from pathlib import Path

import tomli_w

from abara_file_io.common_io_wrapper import common_file_read_exception_handling

log = getLogger(__name__)


def read_toml(path: str | PathLike[str]) -> dict:
    """TOMLファイルを読み込む

        読み込みに失敗した場合は空の辞書を返す

    Args:
        path (Union[Path, str]): 読み込むファイルのパス

    Returns:
        Union[dict, None]:
            正確にはdictのインスタンスのruamel.yaml.comments.CommentedMap
    """

    def read_toml_core(
        f: TextIOWrapper | BufferedReader,
    ) -> dict:
        if isinstance(f, BufferedReader):
            return tomllib.load(f)
        return {}

    return common_file_read_exception_handling(
        func=read_toml_core, return_empty_value={}, file_path=path, mode='rb'
    )


def write_toml(write_data: dict, file_path: str | PathLike) -> None:
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
