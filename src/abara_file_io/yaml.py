#!/usr/bin/env python3
from io import BufferedReader, TextIOWrapper
from logging import getLogger
from os import PathLike
from pathlib import Path

from ruamel.yaml import YAML

from abara_file_io.common_io_wrapper import common_file_read_exception_handling

log = getLogger(__name__)


def read_yaml(path: str | PathLike) -> dict:
    """YAMLファイルの読み込み

        リスト、もしくは辞書型の変数として読み込む
        読み込みに失敗した場合は空の辞書を返す

    Args:
        path (Union[Path, str]): 書き込むファイル名

    Returns:
        Union[dict, None]:
            正確にはdictのインスタンスのruamel.yaml.comments.CommentedMap
    """

    def read_yaml_core(
        f: TextIOWrapper | BufferedReader,
    ) -> dict:
        yaml = YAML()
        if isinstance(f, TextIOWrapper):
            return yaml.load(f)
        return {}

    return common_file_read_exception_handling(
        func=read_yaml_core, return_empty_value={}, path=path
    )


def write_yaml(data: list | dict, file_path: str | PathLike, *, crlf_flag: bool = False) -> None:
    """YAMLファイルとして出力する

        第一引数で受け取ったパスに、第二引数で受け取った内容をYAMLとして書き込む。

    Args:
        data (list | dict): _description_
        file_path (str | PathLike): _description_
        crlf_flag (bool, optional): _description_. Defaults to False.
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    try:
        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)

        path_obj = Path(file_path)

        if crlf_flag is False:
            with path_obj.open(mode='w', encoding='utf-8', newline='\n') as yaml_file:
                yaml.dump(data, yaml_file)
        else:
            with path_obj.open(mode='w', encoding='utf-8') as yaml_file:
                yaml.dump(data, yaml_file)
    except PermissionError:
        log.exception(f'書き込みファイル名が正しく指定されていません: {file_path}')


if __name__ == '__main__':
    pass
